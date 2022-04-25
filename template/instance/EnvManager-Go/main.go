package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net"
	"os"
	"runtime/pprof"
	"sync"
	"time"

	pb "github.com/VegeWong/EnvManager-Go/protobuf"
	queue "github.com/VegeWong/EnvManager-Go/queue"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/keepalive"
)

type DataBufferServer struct {
	pb.UnimplementedDataBufferServer
}

type Record struct {
	eid int64
	tid int64
}

var kacp = keepalive.ClientParameters{
	Time:                10 * time.Second,
	Timeout:             time.Second,
	PermitWithoutStream: true,
}

var configPath = flag.String("config", "conf.json", "Path to config file")
var timeout = flag.Int("timeout", -1, "Manager service time before exit")
var profile = flag.String("profile", "", "profile output")
var ServicePort = flag.Int("port", 9080, "Buffer service port")

var ObsQueue queue.Queue = queue.CreateQueue(10000)
var ActQueue queue.Queue = queue.CreateQueue(10000)
var RecQueue queue.Queue = queue.CreateQueue(100000)
var VarMutex *sync.Mutex = &sync.Mutex{}
var ActiveEnvCounter int64
var Addr2Eids map[string]*[]int64 = make(map[string]*[]int64)
var Eid2Addr map[int64]*string = make(map[int64]*string)
var Addr2Conn map[string]*grpc.ClientConn = make(map[string]*grpc.ClientConn)
var EpisodeBuffer map[int64][][]*pb.Array = make(map[int64][][]*pb.Array)
var EnvStatus map[int64]*bool = make(map[int64]*bool)
var MaxSize int64 = 128

type Schema struct {
	Addr   string
	Config map[string]int64
}

type EnvIDRange struct {
	start int64
	end   int64
	addr  string
	conn  *grpc.ClientConn
}

func CheckStatus(client pb.EnvManageRPCClient) bool {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	res, err := client.Check(ctx, &pb.Request{}, grpc.WaitForReady(true))
	var status bool = res.Status
	if err != nil || !status {
		status = false
	}
	return status
}

func CreateEnv(client pb.EnvManageRPCClient, baseId int64, schema *map[string]int64) (int64, int64) {
	ctx, cancel := context.WithTimeout(context.Background(), 10000*time.Second)
	defer cancel()
	var configs []*pb.EnvConfig
	for mapName, mapThreads := range *schema {
		configs = append(configs, &pb.EnvConfig{
			MapName:    mapName,
			NumThreads: mapThreads,
		})
	}

	res, err := client.CreateEnv(ctx, &pb.EnvSchema{BaseId: baseId, Configs: configs})
	if err == nil {
		return res.EndId, res.Status
	} else {
		return -1, -1
	}
}

func ResetEnv(client pb.EnvManageRPCClient, eids *[]int64) {
	ctx, cancel := context.WithTimeout(context.Background(), 10000*time.Second)
	defer cancel()

	stream, err := client.ResetEnv(ctx)
	if err != nil {
		fmt.Printf("%v call ResetEnv error %v", client, err)
	}
	waitc := make(chan struct{})

	// Receive reset observation
	go func() {
		for {
			envReply, err := stream.Recv()
			if err == io.EOF {
				close(waitc)
				return
			}
			if err != nil {
				log.Printf("Receive error in reset envs %v", err)
				break
			}
			eid := envReply.Column.EnvId
			array := envReply.Column.Array
			EpisodeBuffer[eid] = append(EpisodeBuffer[eid], array)
			*EnvStatus[eid] = envReply.Column.Done
			VarMutex.Lock()
			ActiveEnvCounter += 1
			VarMutex.Unlock()
			ts := int64(len(EpisodeBuffer[eid]) - 1)
			var inferArrays []*pb.Array
			fmt.Printf("Got reset Reply eid: %v \n", eid)
			inferArrays = append(inferArrays, array[0], array[1])
			ObsQueue.Push(&pb.EnvArray{
				EnvId:     eid,
				TimeSteps: ts,
				Array:     inferArrays,
			})
		}
	}()

	for _, eid := range *eids {
		resetReq := pb.ResetRequest{
			Request: &pb.EnvArray{EnvId: int64(eid)},
		}
		fmt.Printf("Reseting env_id %v, %v, %p\n", int64(eid), eid, eids)
		if err := stream.Send(&resetReq); err != nil {
			fmt.Printf("%v stream send reset req on %v error %v", stream, eid, err)
		}
	}
	if err := stream.CloseSend(); err != nil {
		fmt.Println(err)
	}
	<-waitc
}

func StepEnv(client pb.EnvManageRPCClient, agentDecisions []*pb.AgentDecision) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	stream, err := client.StepEnv(ctx)
	if err != nil {
		fmt.Printf("Error in creating context: %v", err)
	}
	waitc := make(chan struct{})

	go func() {
		for {
			envReply, err := stream.Recv()
			if err == io.EOF {
				close(waitc)
				return
			}
			if err != nil {
				fmt.Printf("Receive error in steping envs %v", err)
			}
			done := envReply.Column.Done
			eid := envReply.Column.EnvId
			array := envReply.Column.Array
			tail := len(EpisodeBuffer[eid]) - 1
			transPtr := EpisodeBuffer[eid][tail]
			transPtr = append(transPtr, array[2])
			ts := int64(len(EpisodeBuffer[eid]) - 1)
			RecQueue.Push(&Record{
				eid: eid,
				tid: ts,
			})
			*EnvStatus[eid] = done

			if done {
				VarMutex.Lock()
				ActiveEnvCounter -= 1
				VarMutex.Unlock()
				continue
			} else {
				var inferArrays []*pb.Array
				inferArrays = append(inferArrays, array[0], array[1])
				ObsQueue.Push(&pb.EnvArray{
					EnvId:     eid,
					TimeSteps: ts,
					Array:     inferArrays,
				})
			}
		}
	}()

	for _, decision := range agentDecisions {
		fmt.Printf("Send decision with id %v \n", decision.Action.EnvId)
		stream.Send(decision)
	}
	if err := stream.CloseSend(); err != nil {
		fmt.Println(err)
	}
	<-waitc
}

func InitConnsAndEnvs(configs *[]Schema) {
	var counter int64 = 0
	var baseId int64 = 0
	var conn *grpc.ClientConn

	createc := make(chan EnvIDRange)
	for _, config := range *configs {
		var err error
		conn, err = grpc.Dial(config.Addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err != nil {
			log.Fatalf("Dailing %v fails, skip", config.Addr)
		}
		client := pb.NewEnvManageRPCClient(conn)
		status := CheckStatus(client)

		if status {
			counter += 1
			go func(client pb.EnvManageRPCClient, baseId int64, config Schema, conn *grpc.ClientConn) {
				endId, statusCode := CreateEnv(client, baseId, &config.Config)
				if statusCode == 1 {
					createc <- EnvIDRange{baseId, endId, config.Addr, conn}
				} else {
					createc <- EnvIDRange{baseId, baseId, config.Addr, conn}
				}
			}(client, baseId, config, conn)
		} else {
			log.Fatalf("Pre-launch check for server %v fails, skip", config.Addr)
		}

		var expectedThreads int64 = 0
		for _, mapThreads := range config.Config {
			expectedThreads += mapThreads
		}
		baseId += expectedThreads
	}
	log.Println("Initializing remote servers...")

	/*
		non-parallel code due to golang restriction on
		concurrent writes of maps
	*/
	var totalNum int64 = counter
	for {
		if counter == 0 {
			break
		}
		envr := <-createc
		counter -= 1
		Addr2Conn[envr.addr] = envr.conn
		curEids := Addr2Eids[envr.addr]
		var eids = []int64{}
		var addr string = envr.addr
		for i := envr.start; i < envr.end; i++ {
			eids = append(eids, i)
			var status bool = false
			EnvStatus[i] = &status
			Eid2Addr[i] = &addr
		}
		if curEids == nil {
			Addr2Eids[addr] = &eids
		} else {
			*curEids = append(*curEids, eids...)
		}
		log.Printf("Waiting for remote server .... (%v/%v)", totalNum-counter, totalNum)
	}

	log.Println("Address-env mapping listed as follows:")
	for serverAddr, eids := range Addr2Eids {
		log.Printf("\t%v ------- %v", serverAddr, eids)
	}

}

func ResetAll() {
	var eids *[]int64
	for addr, conn := range Addr2Conn {
		client := pb.NewEnvManageRPCClient(conn)
		eids = Addr2Eids[addr]
		if eids != nil {
			log.Printf("Reset envs %v", eids)
			go ResetEnv(client, eids)
		} else {
			log.Printf("Unknown address %v \n", addr)
		}

	}
}

func (s *DataBufferServer) RequestInferBatch(min int64, max int64) (*pb.BlockReply, error) {
	var arrs []*pb.EnvArray
	var err error
	var size int64 = 0
	for {
		// if ObsQueue.Size() < min {
		// 	time.Sleep(10 * time.Millisecond)
		// }

		arr, err := ObsQueue.Pop()
		if err != nil {
			break
		}
		var ptr *pb.EnvArray = arr.(*pb.EnvArray)
		size += 1
		arrs = append(arrs, ptr)

		if size >= MaxSize {
			break
		}
	}
	ready := (len(arrs) != 0)
	end := (ActiveEnvCounter == 0)
	return &pb.BlockReply{
		Ready:   ready,
		End:     end,
		Columns: arrs,
	}, err
}

func (s *DataBufferServer) RequestTrainBatch() (*pb.BlockReply, error) {
	var arrs []*pb.EnvArray
	var err error
	var size int64 = 0
	for {
		arr, err := RecQueue.Pop()
		if err != nil {
			break
		}

		var ptr *Record = arr.(*Record)
		eid := ptr.eid
		tid := ptr.tid
		tran := EpisodeBuffer[eid][tid]
		size += (*tran[0]).Shapes[0]

		if size >= MaxSize {
			break
		}

		arrs = append(arrs, &pb.EnvArray{
			EnvId: eid,
			Type:  "episode_reply",
			Array: tran,
		})

	}
	ready := (len(arrs) != 0)
	end := (ActiveEnvCounter == 0)
	return &pb.BlockReply{
		Ready:   ready,
		End:     end,
		Columns: arrs,
	}, err
}

func (s *DataBufferServer) Request(ctx context.Context, in *pb.BlockDescription) (*pb.BlockReply, error) {
	mode := in.Mode
	minSize := in.MinBlockSize
	MaxSize := in.MaxBlockSize
	if mode == 0 {
		return s.RequestTrainBatch()
	} else {
		return s.RequestInferBatch(minSize, MaxSize)
	}
}

func issueDecisions(decisions *[]*pb.AgentDecision, addr string) {
	conn := Addr2Conn[addr]
	client := pb.NewEnvManageRPCClient(conn)
	StepEnv(client, *decisions)
}

func (s *DataBufferServer) Step(stream pb.DataBuffer_StepServer) error {
	var decisionsPtr *[]*pb.AgentDecision = &[]*pb.AgentDecision{}
	var addrPtr *string = nil

	for {
		decision, err := stream.Recv()
		if err == io.EOF {
			if len(*decisionsPtr) == 0 {
				break
			} else {
				go issueDecisions(decisionsPtr, *addrPtr)
				break
			}
		}

		inAddr := Eid2Addr[decision.Action.EnvId]
		if addrPtr == nil {
			addrPtr = inAddr
		} else {
			if addrPtr != inAddr {
				go issueDecisions(decisionsPtr, *addrPtr)
				addrPtr = inAddr
				decisionsPtr = &[]*pb.AgentDecision{}
			}
		}
		*decisionsPtr = append(*decisionsPtr, decision)
	}
	return nil
}

func serve(server *grpc.Server) {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%v", *ServicePort))
	if err != nil {
		log.Printf("Listen on port %v failed, err %v", *ServicePort, err)
	}
	log.Println("Starting data buffer service...")
	server.Serve(lis)
}

func main() {
	flag.Parse()

	// load json config
	raw, err := ioutil.ReadFile(*configPath)
	if err != nil {
		fmt.Printf("Error in loading %v", err)
	}
	var schemas []Schema
	json.Unmarshal(raw, &schemas)

	// start data buffer service
	server := grpc.NewServer()
	pb.RegisterDataBufferServer(server, &DataBufferServer{})
	go func() {
		serve(server)
	}()

	//
	InitConnsAndEnvs(&schemas)
	go ResetAll()

	if *profile != "" {
		f, err := os.Create(*profile)
		if err != nil {
			log.Fatal(err)
		}
		pprof.StartCPUProfile(f)
		log.Println("start profiling")
		defer pprof.StopCPUProfile()
	}

	if *timeout != -1 {
		select {
		case <-time.After(time.Duration(*timeout) * time.Second):
			return
		}
	} else {
		waitc := make(chan struct{})
		<-waitc
	}

}
