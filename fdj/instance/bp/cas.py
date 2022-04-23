# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint: 模拟CAS服务token

"""
import json
import requests
from flask import Blueprint, request
from ..utils import cf, aes_ecb_decrypted, register, jsonEncoder

bp_cas = Blueprint('bp_cas', __name__, url_prefix='/user-service')


@bp_cas.route('/hello', methods=('Get',))
def index():
    resp = 'Hello, patch cas service'
    return jsonEncoder(resp)


# @bp_cas.route('/login', methods=('POST',))
# def login():
#     """
#         input: {"user": "liuhx25", "password":"test"}
#
#     :return:
#         {"token": "TGT-1803803-ck-nNd-jI"}
#     """
#     import os, base64
#     req_params = request.get_json(force=True)
#     key = base64.b64encode(os.urandom(5)).decode('utf-8')
#     token = '-'.join([req_params['user'], req_params['password'], key])
#     return json.dumps({"token": token})


@bp_cas.route('/login', methods=('POST',))
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
        # params = {'userCode': req_params['user'], 'password': req_params['password']}
        params = {'user': req_params['user'], 'password': req_params['password']}
        headers = {'Content-type': 'application/json'}
        # post to cas
        url = cf.get('authentic', 'tokenUrl')
        # token
        result = requests.post(url, data=json.dumps(params), headers=headers)
        token = json.loads(result.content)['token']
        # register
        params.update({'token': token})
        status = register(params)
        errorInfo = "注册失败" if status != 0 else ""
        resp = {"status": status, "errorInfo": errorInfo, 'data': token}
    except Exception as e:
        resp = {"status": 1, "errorInfo": e}
    return jsonEncoder(resp)
