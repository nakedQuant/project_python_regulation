import multiprocessing

bind = "127.0.0.1:10000"
workers = multiprocessing.cpu_count() * 2 + 1
# reload = True
reload_extra_files = 'conf.ini'
# ps top
proc_name = 'gunicorn_fdj'
chdir = '.'
# workers
workers = 4
# sync eventlet gevent
work_class = 'gevent'
threads = 2
# log - means stdout stderr
accesslog = '-'
errorlog = '-'
loglevel = 'warning'
# Although there are many HTTP proxies available, we strongly advise that you use Nginx.
