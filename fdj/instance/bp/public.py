# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import os
import json
import base64
from flask import abort
from flask import request
from ..db import dbs
from ..utils import validate, extExcel, canParse, count_time, jsonEncoder, torquePercent2torque
from flask import Blueprint

bp_public = Blueprint('bp_public', __name__)
# 静态资源目录 --- 图片
staticDir = os.path.join(os.path.abspath('./instance'), 'static')


@bp_public.route('/hello', methods=('GET',))
@count_time
def index():
    resp = 'hello fdj'
    return jsonEncoder(resp)


@bp_public.route('/getNames', methods=('POST',))
def getNames():
    """
        说明:获取发动机对应的万有特性曲线图片名称
        input: {"token"："test", "time": 16345323525, "sign": "test",
                "params":{
                        "info":
                            {"model": SY375H,
                            "manufacturer":"五十铃"}
                        }
                }

    :return:
            {"data": [
                    "v0.1.0_2021-11-18 9:30:53",
                    "v0.1.1_2021-11-17 9:31:53",
                    "v0.1.2_2021-11-16 9:32:53",
                    "v0.1.3_2021-11-15 9:33:53"]，
             "status":0,
             "errorInfo": ""
            }
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    # retrieve
    result = dbs.retrieve_picNames(req_params['params'])
    resp = {'status': 0, "errorInfo": '', 'data': result}
    return jsonEncoder(resp)


@bp_public.route('/picLoad', methods=('POST',))
def picLoad():
    """
        说明:加载万特性曲线图
        input :
            {"token"："test", "time": 16345323525, "sign": "test",
            "params": {
                    "info":{
                            "picName": "五十铃_485"
                            }
                    }
            }

    :return: '' or btyes
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    #
    params = req_params['params']
    try:
        pic = os.path.join(staticDir, '%s.png' % params['info']['picName'])
        print('picPath', pic)
        # return send_file(picPath)
        with open(pic, 'rb') as f:
            base64_data = base64.b64encode(f.read())
        # 获取对应图片的阈值
        thres = dbs.retreive_picThres(params)
        resp = {'status': 0, 'errorInfo': '',
                'data': {'data': str(base64_data, encoding='utf-8'), 'thres': thres}}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_public.route('/receive', methods=('POST',))
def receive():
    """
        接收前端上传的针对于理论油耗计算的Excel, 后台文件名token_fileName
        input:
            { "token"："test", "time": 16345323525, "sign":"test",
              "params":{
                        "info": {
                                "canCode": 0,
                                "model": SY375,
                                "manufacturer": 五十铃
                                }
                        }
            }'

        return:
            { "status": 0,
              "errorInfo": '',
              "data": [
                        {"brake": 1, "speed":1200, "torque_out": 1100,
                        "torque_max":1300, "hOil": 1600, "appendix_power": 100},
                        {"brake": 2, "speed":1300, "torque_out": 1200,
                        "torque_max":1400, "hOil": 1800, "appendix_power": 100},
                        {"brake": 3, "speed":1400, "torque_out": 1300,
                        "torque_max":1500, "hOil": 1950, "appendix_power": 100},
                        {"brake": 4, "speed":1500, "torque_out": 1500,
                        "torque_max":1700, "hOil": 1900, "appendix_power": 100},
                        {"brake": 5, "speed":1600, "torque_out": 1600,
                        "torque_max":1800, "hOil": 2000, "appendix_power": 100},
                        {"brake": 6, "speed":1700, "torque_out": 1800,
                        "torque_max":2000, "hOil": 2100, "appendix_power":100},
                        {"brake": 7, "speed":1800, "torque_out": 1900,
                        "torque_max":2100, "hOil": 2200, "appendix_power":100},
                        {"brake": 8, "speed":1900, "torque_out": 2100,
                        "torque_max":2200, "hOil": 2300, "appendix_power":100},
                        {"brake": 9, "speed":2100, "torque_out": 2300,
                        "torque_max":2500, "hOil": 2500, "appendix_power":100},
                        {"brake": 10, "speed":2200, "torque_out": 2600,
                        "torque_max":2800, "hOil": 2700, "appendix_power":100},
                        {"brake": 11, "speed":2400, "torque_out": 3100,
                        "torque_max":3300, "hOil": 2900, "appendix_power":100}
                        ]
            }
    """
    # import pdb
    # pdb.set_trace()
    req_params = json.loads(request.form['data'])
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    #
    try:
        file = request.files.get('file')
        fileName = '_'.join([req_params['token'], file.filename])
        p = os.path.join(os.path.abspath('instance/tmp/theory'), fileName)
        if not os.path.exists(p):
            file.save(p)
        # 解析数据
        canCode = req_params['params']['info']['canCode']
        if canCode == 0:
            result = extExcel(p)
            resp = {'status': 0, 'errorInfo': '',
                    'data': list(result.T.to_dict().values())}
        else:
            result = canParse(p)
            # transform torque% to torque
            points = torquePercent2torque(result[-1], req_params['params']['info'])
            resp = {'status': 0, 'errorInfo': '',
                    'data': list(result.T.to_dict().values()), 'points': points}
        print('resp', resp)
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_public.route('/inputEngine', methods=('POST',))
def inputEngine():
    """
        params = [{"model": "SY375H", "manufacturer": "五十铃"}]
    :return:
    """
    try:
        req_params = request.get_json(force=True)
        dbs.add_engines(req_params)
        resp = {'status': 0, 'errorInfo': ''}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)
