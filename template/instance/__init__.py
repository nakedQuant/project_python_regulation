# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

"""
import os
from flask import Flask
# from .db import dbs
# from .utils import cf

# def init_app_command(app):
#     # method需要在实例中注册, 使用了工厂函数，在函数中进行注册。
#     app.cli.add_command(cli)
#     app.cli.add_command(init_db_command)
#     app.cli.add_command(enroll)
#     app.cli.add_command(enroll_tree)
#     app.cli.add_command(enroll_html)
#     app.cli.add_command(generate_firmware_password)
#     app.cli.add_command(reset)
#     # after_request(response)正常情况下退出
#     # app.teardown_request(shutdown_session)
#     app.teardown_appcontext(shutdown_session)


def create_app(config=None):
    """
        factory instead of global class
        __name__ : python module name
        instance_relative_config :
    """
    app = Flask(__name__, instance_relative_config=True)
    # 设置缺省值配置
    app.config.from_mapping(
        SECRET_KEY='dev_test',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # # 重载缺省值配置 实现开发与测试隔离
    # if config is None:
    #     # silent --- not testing
    #     # app.config.from_pyfile('config.Config.py', silent=True)
    #     # app.config.from_envvar('')
    #     app.config.from_object('config.Config')
    # else:
    #     app.config.from_mapping(config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # 初始化蓝图 --- 注册 登陆 注销
    from .bp import bps

    # add common prefix --- /apis/v1
    for b in bps:
        app.register_blueprint(b)
    # 初始化
    # init_app_command(app)
    return app
