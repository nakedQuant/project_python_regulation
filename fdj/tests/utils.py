# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

"""
import unittest
import sys
from pathlib import Path
import requests
import json


def req(param, endPoint, files):
    pJson = json.dumps(param, ensure_ascii=False).encode('utf-8')
    url = "http://{}:{}/".format('localhost', 10000) + endPoint
    if files:
        response = requests.post(url, {'data': pJson}, files=files) if isinstance(files, dict) else \
            requests.post(url, {'data': pJson, 'file': files})
    else:
        response = requests.post(url, data=pJson, headers={'Content-type': 'application/json'})
    print('response', response.text)
    response = json.loads(response.text)
    return response['status']
