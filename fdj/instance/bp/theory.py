# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:静态匹配
"""
from flask import Blueprint, request, abort
from ..db import dbs
from ..utils import validate, formatOutput, parseTheory, engineProperty, jsonEncoder
from ..algorithm import predict


bp_theory = Blueprint('bp_theory', __name__, url_prefix='/theory')


@bp_theory.route('/hello', methods=('Get',))
def index():
    resp = 'Hello, 静态匹配'
    return jsonEncoder(resp)


@bp_theory.route('/getPlans', methods=('POST',))
def getPlans():
    """
        说明: 基于机型类型获取所有的方案信息
        input: {"token"："test", "time": 16345323525, "sign": "test",
                "params": {
                            "info":{
                                    "model": SY375H,
                                    "manufacturer":"五十铃"
                                    }
                            }
                }

    :return:
            { "status": 0,
              "errorInfo": "",
              "data": {'plan':[{'planName':1,
                                'data':[{"planVersion":'第一次测试_2021-12-08 11:33:10.549699'},
                                       {"planVersion":'第一次测试_1_2021-12-08 12:53:11.220600'}]},
                              {'planName':2,
                                'data':[{'planVersion':'第一次测试_1_2021-12-08 13:00:10.699312'}]}]
                    }
    """
    req_params = request.get_json(force=True)
    params = req_params['params']
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    # 获取方案
    print('getplan params', params)
    try:
        frame = dbs.retrieve_planNames(params)
        # print('frame', frame.head())
        result = formatOutput(frame)
        # print('result', result)
        resp = {'status': 0, 'errorInfo': '', 'theory': result}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_theory.route('/planLoad', methods=('POST',))
def planLoad():
    """
        说明:基于方案名称和版本加载对应的方案内容
        input:
            {"token"："test", "time": 16345323525, "sign": "abcdfe345325346efdthgfagds",
             "params":{
                    "info":{"planVersion": "第一次测试_2021-12-08 09:49:23" }
                    }

    :return:
            { "status": 0,
              "errorInfo": '',
              "theory":{
                    "info": {
                            "picName": "v0.2.1"
                            },
                    "data":[
                            {"brake": 1, "speed":1300, "torque_out": 1100, "torque": 1200, "torque_max": 1300,
                            "hydraulic_power":2500, "engine_power": 2100,"engine_full_power": 2600,
                            "appendix_power": 500, "engine_property_torque": 1400, "engine_property_power": 2700,
                            "saturation": 0.75, "oil": 3.2, "theory_hOil": 35, "hOil": 48, "revise": 0.65},
                            {"brake": 2, "speed":1400, "torque_out": 1300, "torque": 1500, "torque_max": 1300,
                            "hydraulic_power":2800, "engine_power": 2400,"engine_full_power": 3000,
                            "appendix_power": 700, "engine_property_torque": 1600, "engine_property_power": 3100,
                            "saturation": 0.80, "oil": 3.5, "theory_hOil": 37, "hOil": 50, "revise": 0.70}
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
    try:
        result = dbs.retrieve_plans(params)
        resp = {'status': 0, 'errorInfo': '', 'data': result}
    except Exception as e:
        print('e', e)
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_theory.route('/calculate', methods=('POST',))
def calculate():
    """
        说明: 档位、转数、泵输入扭矩、发动机总输入功率计算
              1、发动机外特性扭矩（万有特性曲线上线） ---- 基于模型得出
              2、发动机外特性功率 = 转速 * 发动机外特性扭矩 / 9549
              3、匹配饱和度 = 泵输入扭矩 / 发动机外特性扭矩
              4、理论小时油耗（L / h ) = 理论油耗比值 * 发动机总输入功率 / 850
              5、修正系数 = 理论小时油耗 / 实际小时油耗

        input :
            {"token"："test", "time": 16345323525, "sign": "test",
            "params":{
                    "info":{
                            "picName": "五十铃_SY375H"
                          },
                    "data":[
                            {"brake": 1, "speed":1000, "torque_out": 1400, "appendix_power": 100, "hOil": 32},
                            {"brake": 2, "speed":1200, "torque_out": 1500, "appendix_power": 105, "hOil": 33},
                            {"brake": 3, "speed":1300, "torque_out": 1600, "appendix_power": 107, "hOil": 34},
                            {"brake": 4, "speed":1400, "torque_out": 1700, "appendix_power": 115, "hOil": 35},
                            {"brake": 5, "speed":1500, "torque_out": 1800, "appendix_power": 117, "hOil": 36},
                            {"brake": 6, "speed":1600, "torque_out": 1900, "appendix_power": 118, "hOil": 37},
                            {"brake": 7, "speed":1700, "torque_out": 2000, "appendix_power": 120, "hOil": 38},
                            {"brake": 8, "speed":1800, "torque_out": 2100, "appendix_power": 130, "hOil": 39},
                            {"brake": 9, "speed":1900, "torque_out": 2200, "appendix_power": 140, "hOil": 41}
                        ]
                    }
            }

    :return:
            {"status":0,
             "errorInfo": "",
             "data":[
                    {"brake": 1, "torque": 1200, "hydraulic_power":2500, "engine_power": 2100,
                    "engine_full_power": 2600, "engine_property_torque": 1400, "engine_property_power": 2700,
                    "saturation": 0.75, "oil": 3.2, "theory_hOil": 35, "revise": 0.65},
                    {"brake": 2, "torque": 1500, "hydraulic_power":2800, "engine_power": 2400,
                    "engine_full_power": 3000, "engine_property_torque": 1600, "engine_property_power": 3100,
                    "saturation": 0.80, "oil": 3.5, "theory_hOil": 37, "revise": 0.70}
                    ]
             }
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    # model input
    info = req_params['params']['info']
    data = parseTheory(req_params['params']['data'])
    info.update({'data': data})
    # load model and calculate
    try:
        # 计算理论油耗
        f = predict(info)
        print('oil', f.head())
        # 外特性特征
        result = engineProperty(f)
        print('result', result.head())
        # del speed  torque_out appendix_power hOil
        result.drop(["speed", "torque_out", "appendix_power", "hOil", 'max_torque'], axis=1, inplace=True)
        resp = {'status': 0, 'errorInfo': '', 'data': list(result.T.to_dict().values())}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_theory.route('/save', methods=('POST',))
def save():
    """
        说明: 保存理论油耗计算方案
        input:
                {"token"："test", "time": 16345323525, "sign": "test",
                "params":{
                            "info":{
                                  "model": "SY375H",
                                  "manufacturer": "五十铃",
                                  "picName": "v0.1.2_2021-10-30 12:20:30",
                                  "planName": "1",
                                  "planVersion": "v0.1.2"
                              },
                            "data":[
                                {"brake": 1, "speed":1300, "torque_out": 1100, "torque": 1200, "torque_max": 1300,
                                "hydraulic_power":2500, "engine_power": 2100,"engine_full_power": 2600,
                                "appendix_power": 500, "engine_property_torque": 1400, "engine_property_power": 2700,
                                "saturation": 0.75, "oil": 3.2, "theory_hOil": 35, "hOil": 48, "revise": 0.65},
                                {"brake": 2, "speed":1400, "torque_out": 1300, "torque": 1500, "torque_max": 1600,
                                "hydraulic_power":2800, "engine_power": 2400,"engine_full_power": 3000,
                                "appendix_power": 700, "engine_property_torque": 1600, "engine_property_power": 3100,
                                "saturation": 0.80, "oil": 3.5, "theory_hOil": 37, "hOil": 50, "revise": 0.70},
                                ]
                        }
                }

    :return: {
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
    try:
        dbs.save_plans(req_params['params'])
        resp = {'status': 0, 'errorInfo': ''}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)
