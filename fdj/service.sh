#rm -rf /var/lib/mysql/mysql.sock.lock
#nohup mysqld &
#nohup redis-server &
#cd /root/cas && nohup gunicorn -w 10 -b localhost:20000 service:app &
cd /root/fdj && nohup python3 runinit.py &
