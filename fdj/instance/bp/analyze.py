# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:曲线对比

"""
from flask import Blueprint, request, abort
from ..algorithm import predict
from ..utils import validate, jsonEncoder


bp_analyze = Blueprint('bp_analyze', __name__, url_prefix='/analyze')


@bp_analyze.route('/hello', methods=('Get',))
def index():
    resp = 'Hello, 曲线对比'
    return jsonEncoder(resp)


@bp_analyze.route('/calculate', methods=('POST',))
def calculate():
    """
        说明: 基于转速、扭矩计算不同发动机类型的理论比油耗值
        input:
            {"token"："test", "time": 16345323525, "sign": "test",
            "params":{
                    "info":{
                            "model1": {
                                    "picName": "五十铃_SY375H"},
                            "model2":{
                                    "picName": "五十铃_485"}
                            },
                    "data":[
                            {"brake":1, "speed":1000, "torque":1500},
                            {"brake":2, "speed":1100, "torque":1600},
                            {"brake":3, "speed":1200, "torque":1700},
                            {"brake":4, "speed":1300, "torque":1800}
                            ]
                    }
            }

    :return:
            {"status": 0,
             "errorInfo" "",
             "data":{
                    "model1":[
                                {"brake": 1, "oil": 3.5},
                                {"brake": 2, "oil": 3.6},
                                {"brake": 3, "oil": 3.8},
                                {"brake": 4, "oil": 4.2},
                                {"brake": 5, "oil": 4.5}
                             ],
                    "model2":[
                                {"brake": 1, "oil": 3.6},
                                {"brake": 2, "oil": 3.7},
                                {"brake": 3, "oil": 3.9},
                                {"brake": 4, "oil": 4.4},
                                {"brake": 5, "oil": 4.6}
                             ]
                    }
            }
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)

    params = req_params['params']
    data = params['data']
    print('before theory', data)
    # 将输出扭矩转为输入扭矩
    [item.update({'torque': item['torque'] / 0.85}) for item in data]
    print('transform theory', data)
    c1Param = params['info']['model1']
    c1Param.update({'data': data})
    c2Param = params['info']['model2']
    c2Param.update({'data': data})
    try:
        result1 = predict(c1Param)
        out1 = list(result1.loc[:, ['brake', 'oil']].T.to_dict().values())
        print('output', out1)
        result2 = predict(c2Param)
        out2 = list(result2.loc[:, ['brake', 'oil']].T.to_dict().values())
        print('output', out2)
        data = {'model1': out1, 'model2': out2}
        resp = {'status': 0, 'errorInfo': '', 'data': data}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)
