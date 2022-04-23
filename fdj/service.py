# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
from flask_cors import CORS
from instance import create_app
from instance.utils import cf

# from flask import g
# def get_db_con():
#     # g --- 特殊对象，独立于每一次请求，在处理请求的过程中存储多个函数用到的数据多次使用， 不同一个请求get_db产生一个新的链接
#     if 'db' not in g:
#         # ensure avoiding no database selected
#         eng_obj = init_engine()
#         g.db = eng_obj.connect()
#     return g.db
#

# def shutdown_session(exception):
#     session = g.pop('db_session', None)
#     if session:
#         session.close()


app = create_app()
# 跨域
CORS(app, supports_credentials=True)


if __name__ == "__main__":

    # dipose all connection when service shutsdown
    # import atexit
    # from instance import dbs
    # atexit.register(dbs.atexit)
    # 服务
    app.run(host=cf.get('service', 'FLASK_IP'),
            port=cf.get('service', 'FLASK_PORT'),
            threaded=True, debug=True)
