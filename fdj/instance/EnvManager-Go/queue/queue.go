package queue

import (
	"errors"
	"sync"
)

type Queue struct {
	maxSize int64
	curSize int64
	array   []interface{}
	head    int64
	tail    int64
	mut     *sync.Mutex
}

func CreateQueue(maxSize int64) Queue {
	return Queue{
		maxSize: maxSize,
		curSize: 0,
		array:   make([]interface{}, maxSize),
		head:    0,
		tail:    0,
		mut:     &sync.Mutex{},
	}
}

func (q *Queue) Size() (int64) {
	q.mut.Lock()
	defer q.mut.Unlock()
	return q.curSize
}

func (q *Queue) Push(elem interface{}) error {
	q.mut.Lock()
	defer q.mut.Unlock()

	if q.curSize < q.maxSize {
		q.array[q.tail] = elem
		q.tail = (q.tail + 1) % q.maxSize
		q.curSize += 1
		return nil
	} else {
		return errors.New("Queue length exceeds maxSize limitation")
	}
}

func (q *Queue) Pop() (interface{}, error) {
	q.mut.Lock()
	defer q.mut.Unlock()

	if q.curSize > 0 {
		curHead := q.head
		q.head = (q.head + 1) % q.maxSize
		q.curSize -= 1
		return q.array[curHead], nil
	} else {
		return nil, errors.New("Queue empty")
	}
}

func (q *Queue) IsEmpty() bool {
	q.mut.Lock()
	defer q.mut.Unlock()

	if q.curSize > 0 {
		return false
	} else {
		return true
	}
}
