# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint: 模拟CAS服务token

"""
from flask import Blueprint, request
from ..utils import cf, aes_ecb_decrypted, register, jsonEncoder, cas_token

bp_cas = Blueprint('bp_cas', __name__, url_prefix='/user-service')


@bp_cas.route('/hello', methods=('Get',))
def index():
    resp = 'Hello, patch cas service'
    return jsonEncoder(resp)


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
        token, params = cas_token(req_params)
        # register
        params.update({'token': token})
        status = register(params)
        errorInfo = "注册失败" if status != 0 else ""
        resp = {"status": status, "errorInfo": errorInfo, 'data': token}
    except Exception as e:
        resp = {"status": 1, "errorInfo": e}
    return jsonEncoder(resp)
