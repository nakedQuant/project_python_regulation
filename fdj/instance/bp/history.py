# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:历史结果分析
"""
import json
import os
from flask import Blueprint, request, abort
from ..utils import validate, whereis, figureLines, fetch, resample, jsonEncoder, canParse


bp_history = Blueprint('bp_history', __name__, url_prefix='/historyAnalysis')


@bp_history.route('/hello', methods=('Get',))
def index():
    resp = 'Hello, 历史结果分析'
    return jsonEncoder(resp)


@bp_history.route('/upload', methods=('POST',))
def upload():
    """
        接收并保存前端上传的数据源文件
        input:
            { "token"："test", "time": 16345323525, "sign":"test",
              "params":{}
            }

        return:
            { "status": 0,
              "errorInfo": ''
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
    try:
        # 可以覆盖相同的文件
        file = request.files.get('file')
        name = '_'.join([req_params['token'], file.filename])
        p = os.path.join(os.path.abspath('./instance/tmp/history/source'), name)
        file.save(p)
        result, points = canParse(p)
        resp = {'status': 0, 'errorInfo': '', 'data': result}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_history.route('/conf', methods=('POST',))
def conf():
    """
        接收前端上传的配置文件
        input:
            { "token"："test", "time": 16345323525, "sign":"test",
              "params":{
                        "info": {
                                "source":"test"
                                }
            }

        return:
            { "status": 0,
              "errorInfo": '',
              "data": [1,2,3,4,5,7,8,9,10]
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
    # 判断数据源是否存在
    source = req_params['params']['info']['source']
    if not whereis(req_params['token'], source, 'source'):
        resp = {'status': 1, 'errorInfo': '缺少数据源'}
        return json.dumps(resp, ensure_ascii=False, indent=4)
    try:
        # 可以覆盖相同的文件
        file = request.files.get('file')
        original = file.filename
        fileName = '_'.join([req_params['token'], original])
        p = os.path.join(os.path.abspath('./instance/tmp/history/conf'), fileName)
        file.save(p)
        # parse conf and source
        f1, f2 = fetch(req_params['token'], source, original)
        # resample and transform to str
        sampling = resample(f1)
        sampling = [s.strftime('%Y-%m-%d %H:%M:%S.%f') for s in sampling]
        data = {'time': sampling, 'figures': list(f2['figure'].unique())}
        resp = {'status': 0, 'errorInfo': '', 'data': data}
        print('resp', resp)
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)


@bp_history.route('/figure', methods=('POST',))
def figure():
    """
    根据figure、配置与数据源名称返回对应的subplots与数据
    input:
        { "token"："test", "time": 16345323525, "sign":"test",
          "params":{
                    "info":{
                            "figure": "1",
                            "conf" "test",
                            "source": "test"
                            }
                    }
        }

    :return:
            {"status": 0,
             "errorInfo": ''，
             "data": {
                    "铲斗挖掘手柄": {1:}
                    "铲斗卸载手柄": {2:}
                     }
    """
    req_params = request.get_json(force=True)
    # 验证
    status = validate(req_params)
    # status = 0
    if status != 0:
        abort(status)
    try:
        info = req_params['params']['info']
        # token = req_params['token']
        info.update({'token': req_params['token']})
        # result = figureLines(info, token)
        result = figureLines(info)
        resp = {'status': 0, 'errorInfo': '', 'data': result}
    except Exception as e:
        resp = {'status': 1, 'errorInfo': e.args[-1]}
    return jsonEncoder(resp)
