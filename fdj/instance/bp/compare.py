# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:动态匹配
"""
from flask import Blueprint, request, abort
from ..utils import validate, jsonEncoder
from ..db import dbs
from ..algorithm import predict


bp_compare = Blueprint('bp_compare', __name__, url_prefix='/compare')


@bp_compare.route('/hello', methods=('Get',))
def index():
    resp = 'Hello, 动态匹配'
    return jsonEncoder(resp)


@bp_compare.route('/getPlans', methods=('POST',))
def getPlans():
    """
        说明: 获取动态多点匹配的方案
        input:
            {"token"："test", "time": 16345323525, "sign": "abcdfe345325346efdthgfagds",
            "params":{
                    "info":{
                            "model": SY375H，
                            "manufacturer": "五十铃"
                            }
                     }
            }

    :return:
            { "status": 0,
              "errorInfo": '',
              "data":[
                      "v0.0.1_2021-11-18 9:30:53",
                      "v0.0.2_2021-11-17 9:30:53",
                      "v0.0.3_2021-11-16 9:30:53",
                      "v0.0.4_2021-11-15 9:30:53"
                    ]
            }
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    params = req_params['params']
    try:
        result = dbs.retrieve_matchplanNames(params)
        print('result', result)
        resp = {'status': 0, 'errorInfo': '', 'data': result}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_compare.route('/planLoad', methods=('POST',))
def planLoad():
    """
        说明: 动态多点匹配方案加载
    input:
            {"token"："test", "time": 16345323525, "sign": "abcdfe345325346efdthgfagds",
            "params":{
                    "info":{"matchPlan": "第一次对比测试方案_2021-12-08 10:23:15"}
                     }
            }

    :return:
            { "status": 0,
              "errorInfo": '',
              "data":{
                    "info":{
                            "model": SY375H,
                            "manufacturer": "五十铃"
                          }
                    "data":
                         [{"time":"2021-11-30 19:56:00.049034", "speed":1000, "torsion(%)":0.65,
                         "cumOil": 6, "oilFlow": 6.3},
                          {"time":"2021-11-30 19:57:00.049034", "speed":2000, "torsion(%)":0.72,
                          "cumOil": 7, "oilFlow": 7.2},
                          {"time":"2021-11-30 19:58:00.049034", "speed":3000, "torsion(%)":0.85,
                          "cumOil": 8, "oilFlow": 8.2}],
                    "points":
                        [[1000, 1100], [1200, 1300], [1400, 1500], [1500, 1600]]
                    }
            }
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
        result = dbs.retrieve_matchplans(params)
        resp = {'status': 0, 'errorInfo': '', 'data': result}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_compare.route('/calculate', methods=('POST',))
def calculate():
    """
        说明: 根据档位、转数、扭矩计算对应的理论比油耗值，理论比油耗值/h, 实际油耗值/h
        input:
            {"token"："test", "time": 16345323525, "sign": "test",
            "params":{
                    "info":{
                            "picName": "五十铃_SY375H"
                            },
                    "data":[
                          {"time":"2021-11-30 19:55:12.498", "speed":1000, "torque(%)":0.65},
                          {"time":"2021-11-30 19:56:12.510", "speed":1100, "torque(%)":0.69},
                          {"time":"2021-11-30 19:57:12.520", "speed":1200, "torque(%)":0.72},
                          {"time":"2021-11-30 19:58:12.530", "speed":1300, "torque(%)":0.79}
                        ]
                    }
            }

    :return:
            {"data": [
                    {"time":"2021-11-30 19:55:00.049034", "torque":1500, "oil": 3.5},
                    {"time":"2021-11-30 19:55:00.049034", "torque":1600, "oil": 3.6},
                    {"time":"2021-11-30 19:55:00.049034", "torque":1700, "oil": 3.8},
                    {"time":"2021-11-30 19:55:00.049034", "torque":1800, "oil": 4.2},
                    {"time":"2021-11-30 19:55:00.049034", "torque":1900, "oil": 4.5}
                     ]
            "status": 0 ,
            "errorInfo": ""
        }
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    # model input
    params = req_params['params']
    info = params['info']
    info.update({'data': params['data']})
    try:
        result = predict(info, percent=True)
        output = list(result.loc[:, ['time', 'torque', 'oil']].T.to_dict().values())
        resp = {'status': 0, 'errorInfo': '', 'data': output}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_compare.route('/save', methods=('POST',))
def save():
    """
        说明: 保存动态匹配方案
        input:
            {"token"："test", "time": 16345323525, "sign": "abcdfe345325346efdthgfagds",
            "params":{
                     "info":{
                            "model": "SY375H",
                            "manufacturer": "五十铃",
                            "matchPlan": "第二次测试"},
                     "data":[
                            {"time":"2021-11-30 19:56:12.490", "speed":1000, "torque(%)":0.65,
                            "cumOil": 6, "oilFlow": 0.5},
                            {"time":"2021-11-30 19:57:12.510", "speed":2000, "torque(%)":0.72,
                            "cumOil": 7, "oilFlow": 0.6},
                            {"time":"2021-11-30 19:58:12.540", "speed":3000, "torque(%)":0.85,
                            "cumOil": 8, "oilFlow": 0.7}
                            ],
                    "points":
                            [[1000, 1100], [1200, 1300], [1400, 1500], [1500, 1600]]
                    }
            }

    :return: {
            "status": 0 ,
            "errorInfo": ""
            }
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    params = req_params['params']
    try:
        dbs.save_matchplans(params)
        resp = {'status': 0, 'errorInfo': ''}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)
