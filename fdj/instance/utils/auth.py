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
    print('validate', result)
    return result['status']
