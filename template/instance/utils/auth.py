# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import requests
import json
from .cfg import cf


registerUrl = cf.get('authentic', 'registerUrl')
validateUrl = cf.get('authentic', 'validateUrl')
tokenUrl = cf.get('authentic', 'tokenUrl')

# docker
# tokenurl = 'http://cas:20000/cas_service'
# registerurl = 'http://cas:20000/register'
# validateurl = 'http://cas:20000/validate'


def register(params):
    pJson = json.dumps(params, ensure_ascii=False)
    pJson = pJson.encode('utf-8').decode('latin-1')
    req = requests.post(url=registerUrl, data=pJson)
    req.encoding = 'utf-8'
    result = json.loads(req.content)
    return result['status']


def validate(params):
    """
        验证token

    :return:
    """
    pJson = json.dumps(params, ensure_ascii=False)
    # 解码
    pJson = pJson.encode('utf-8').decode('latin-1')
    req = requests.post(url=validateUrl, data=pJson)
    req.encoding = 'utf-8'
    result = json.loads(req.content)
    return result['status']


def cas_token(req_params):
    # params = {'userCode': req_params['user'], 'password': req_params['password']}
    params = {'user': req_params['user'], 'password': req_params['password']}
    headers = {'Content-type': 'application/json'}
    # post to cas token
    result = requests.post(tokenUrl, data=json.dumps(params), headers=headers)
    token = json.loads(result.content)['token']
    # import base64
    # import os
    # key = base64.b64encode(os.urandom(5)).decode('utf-8')
    # token = '-'.join([req_params['user'], req_params['password'], key])
    return token, params
