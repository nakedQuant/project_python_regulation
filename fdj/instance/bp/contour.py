# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:万有特性曲线
"""
import os
import json
import base64
from flask import Blueprint, request, abort
from ..utils import validate, jsonEncoder
from ..db import dbs
from ..algorithm import generateContour, generateModel, generatePickle


bp_contour = Blueprint('bp_contour', __name__, url_prefix='/contour')


@bp_contour.route('/hello', methods=('Get',))
def index():
    resp = 'Hello, 万有特性曲线'
    return jsonEncoder(resp)


@bp_contour.route('/generate', methods=('POST',))
def generate():
    """
        说明: 基于扭矩和转速模拟万有特性曲线图
        input:
            {"token"："test", "time": 16345323525, "sign": "test",
             "params":{
                    "data":[
                            {"Rpm":1000, "Kw":1500, "Nm": 1800, "g/Kwh": 4.2},
                            {"Rpm":1100, "Kw":1600, "Nm": 1900, "g/Kwh": 4.4},
                            {"Rpm":1200, "Kw":1700, "Nm": 2000, "g/Kwh": 4.5},
                            {"Rpm":1300, "Kw":1800, "Nm": 2100, "g/Kwh": 4.6}
                            ]
                     }
            }

    :return: json data
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    # 调用算法生产图片
    try:
        # result = generateContour(req_params['params'])
        result = generateContour(req_params)
        p = result.pop('save_path')
        with open(p, 'rb') as f:
            base64_data = base64.b64encode(f.read())
        # return base64_data
        print('result', result)
        thres = {k: str(v) for k, v in result.items()}
        print('thres', thres)
        resp = {'status': 0, 'errorInfo': '',
                'data': {'thres': thres, 'data': str(base64_data, encoding='utf-8')}}
    except Exception as e:
        resp = {"status": 1, "errorInfo": e.args[-1]}
    return jsonEncoder(resp)


@bp_contour.route('/save', methods=('POST',))
def save():
    """
        input:
            {"token"："test", "time": 16345323525, "sign": "test",
            "params":{
                    "info":{
                            "model": "SY375H",
                            "manufacturer": "五十铃",
                            "picName": "test"
                            },
                    "thres":{
                            "rpm_min":0,
                            "rpm_max":2000,
                            "trq_min":0,
                            "trq_max":2000
                            },
                    "data":{'model': [
                            {"Rpm":1000, "Kw":1500, "Nm": 1800, "g/Kwh": 4.2},
                            {"Rpm":1100, "Kw":1600, "Nm": 1900, "g/Kwh": 4.4},
                            {"Rpm":1200, "Kw":1700, "Nm": 2000, "g/Kwh": 4.5},
                            {"Rpm":1300, "Kw":1800, "Nm": 2100, "g/Kwh": 4.6}
                                    ],
                            'pickle':[
                             {"rpm":1103.8, "Nm":842.6979525},
                             {"rpm":1199.8, "Nm":928.892315385898},
                             {"rpm":1311.5, "Nm":995.413648494091},
                             {"rpm":1400.5, "Nm":1048.07925740807},
                             {"rpm":1500, "Nm":1078.51333333333},
                             {"rpm":1698.9, "Nm":1070.85467066926},
                             {"rpm":1800.1, "Nm":1064.76584634187},
                             {"rpm":2000.8, "Nm":1011.41793282687}
                                    ]
                            }
                    }
            }

    :return: {
            "status": 0 ,
            "errorInfo": ""}
    """
    req_params = json.loads(request.form['data'])
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    params = req_params['params']
    info = params['info']
    pickleData = params['data']['pickle']
    print('info-----', info)
    try:
        # 获取二进制图片数据
        data = request.form['file']
        print('data', data)
        # picture name and save
        picName = '_'.join([info['picName'], req_params['token']])
        p = os.path.join(os.path.abspath('./instance/static'), '%s.png' % picName)
        with open(p, 'wb') as f:
            data = bytes(data, encoding='utf-8')
            data = base64.b64decode(data)
            f.write(data)
        print('write bytes into file png')
        # 更新图片信息
        info['picName'] = picName
        # generate model
        info.update({'data': params['data']})
        generateModel(info)
        # generate pickle
        generatePickle(pickleData, picName)
        # 更新图片阈值信息
        info.update(params['thres'])
        print('contour update info', info)
        dbs.add_picNames(info)
        resp = {"status": 0, "errorInfo": ""}
    except Exception as e:
        resp = {"status": 1, "errorInfo": e.args[-1]}
    return jsonEncoder(resp)
