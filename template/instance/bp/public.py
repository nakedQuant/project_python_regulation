# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import os
import json
import base64
from flask import Blueprint
from flask import abort
from flask import request
from ..db import dbs
from ..utils import validate, count_time, jsonEncoder, aes_ecb_decrypted, register, cas_token

public = Blueprint('public', __name__)


@public.route('/index', methods=('GET',))
@count_time
def index():
    resp = 'hello, public'
    return jsonEncoder(resp)


@public.route('/login', methods=('POST',))
def login():
    """
        input: {"user": "liuhx25", "password":"test"}

    :return:
        {"status": status, "errorInfo": errorInfo, 'data': 'TGT-1803803-ck-nNd-jI'}
    """
    original = request.get_json(force=True)
    # decrypt
    req_params = aes_ecb_decrypted(original)
    print('login api', req_params)
    try:
        token, params = cas_token(req_params)
        # register
        params.update({'token': token})
        status = register(params)
        errorInfo = "注册失败" if status != 0 else ""
        resp = {"status": status, "errorInfo": errorInfo, 'data': token}
    except Exception as e:
        resp = {"status": 1, "errorInfo": e}
    return jsonEncoder(resp)


@public.route('/picLoad', methods=('POST',))
def upload():
    """
        上传图片
        input :
            {"token"："test", "time": 16345323525, "sign": "test",
            "params": { "picName": "test"}
            }

    :return: '' or btyes
    """
    req_params = request.get_json(force=True)
    # 验证
    # status = validate(req_params)
    status = 0
    if status != 0:
        abort(status)
    #
    params = req_params['params']
    try:
        pic = os.path.join(os.path.join(os.path.abspath('./instance'), 'static'), '%s.png' % params['picName'])
        with open(pic, 'rb') as f:
            base64_data = base64.b64encode(f.read())

        resp = {'status': 0, 'errorInfo': '',
                'data': {'data': str(base64_data, encoding='utf-8')}}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    # return send_file(picPath)
    return jsonEncoder(resp)


@public.route('/receive', methods=('POST',))
def download():
    """
        接收并保存前端上传的数据源文件
        input:
            { "token"："test", "time": 16345323525, "sign":"test",
              "params":{}
            }

        return:
            { "status": 0,
              "errorInfo": ''
            }

    """
    # import pdb
    # pdb.set_trace()
    req_params = json.loads(request.form['data'])
    # 验证
    # status = validate(req_params)
    status = 0
    if status != 0:
        abort(status)
    try:
        file = request.files.get('file')
        fileName = '_'.join([req_params['token'], file.filename])
        p = os.path.join(os.path.abspath('instance/static'), fileName)
        if not os.path.exists(p):
            file.save(p)
        # 解析数据
        resp = {'status': 0, 'errorInfo': '',
                'data': 'test'}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)
