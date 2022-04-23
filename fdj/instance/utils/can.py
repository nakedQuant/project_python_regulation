# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import pandas as pd
import pickle
import os
from .file import read


def universe_parse(data, loc, offset=0, unit=1):
    #  解析配置文件里面的对应的can码
    """
    :param data: hex
    :param loc: '3, 4'
    :param offset: 偏移量
    :param unit: 单位
    :return:
    """
    s, e = loc.split(',') if len(loc) == 3 else (loc, loc)
    parts = data.split(' ')[int(s): int(e)]
    count, result = (0, 0)
    for p in parts:
        result = int(p, 16) * (256 ** count) + result
        count = count + 1
    # offset and unit
    result = (result - offset) * unit
    return result


def canParse(fPath):

    def parseTorque(dataH):
        # 解析扭矩百分比 0x18fff800 4 -125 1%
        test = dataH.split(' ')[3]
        torison = int(test, 16) - 125
        # return float(torison / 100)
        return torison

    def parseSpeed(dataH):
        # 解析转速 0xcf00400 4-5 0 0.125
        parts = dataH.split(' ')[3: 5]
        speed = (int(parts[0], 16) + int(parts[1], 16) * 256) / 8
        return speed

    def parseOilFlow(dataH):
        # 燃油流量 18FEF200  1-2  0 0.05L/h
        parts = dataH.split(' ')[0: 2]
        oilFlow = (int(parts[0], 16) + int(parts[1], 16) * 256) * 0.05
        return oilFlow

    def parseCumOil(dataH):
        # 累计燃油使用量 18FEE900 5-8 0 0.5L
        parts = dataH.split(' ')[4: 8]
        cumOil = (int(parts[0], 16) + int(parts[1], 16) * 256 + int(parts[2], 16) * (256 ** 2) + int(parts[3], 16) * (
                    256 ** 3)) / 2
        return cumOil

    # calculate
    frame = read(fPath)
    f = frame.loc[:, ['WRITE_TIME', 'MAKE_CAN_ID(HEX)', 'DATA(HEX)']]
    f.index = f['WRITE_TIME'].apply(lambda x: x[1:-1])
    # 解析部分
    torque = f['DATA(HEX)'][f['MAKE_CAN_ID(HEX)'] == '0x18fff800'].apply(lambda x: parseTorque(x))
    torque.name = 'torque(%)'
    print('torque(%)', torque)
    speed = f['DATA(HEX)'][f['MAKE_CAN_ID(HEX)'] == '0xcf00400'].apply(lambda x: parseSpeed(x))
    print('speed', speed)
    speed.name = 'speed'
    oilFlow = f['DATA(HEX)'][f['MAKE_CAN_ID(HEX)'] == '0x18fef200'].apply(lambda x: parseOilFlow(x))
    print('oilFlow', oilFlow)
    oilFlow.name = 'oilFlow'
    cumOil = f['DATA(HEX)'][f['MAKE_CAN_ID(HEX)'] == '0x18fee900'].apply(lambda x: parseCumOil(x))
    print('cumOil', cumOil)
    cumOil.name = 'cumOil'
    # points (speed and torque%)
    points = zip(speed.values.tolist(), torque.values.tolist())
    # drop duplicates index
    oilFlow = oilFlow[~oilFlow.index.duplicated(keep='last')]
    # reindex 流量频率低于转速、扭矩百分比
    bench = oilFlow.index
    torque = torque[~torque.index.duplicated(keep='last')]
    torque = torque.reindex(bench)
    speed = speed[~speed.index.duplicated(keep='last')]
    speed = speed.reindex(bench)
    # 由于流量的采样频率高于累计燃油值，需要单独处理index
    cumOil = cumOil[~cumOil.index.duplicated(keep='last')]
    freq = int(len(oilFlow) / len(cumOil))
    cumOil.index = bench[::freq][:len(cumOil)]
    cumOil = cumOil.reindex(bench)
    # concat
    result = pd.concat([torque, speed, oilFlow, cumOil], axis=1)
    # result.dropna(how='any', inplace=True, axis=1)
    result.fillna(method='bfill', inplace=True)
    result.fillna(method='ffill', inplace=True)
    result.loc[:, 'time'] = result.index
    print('result', len(result), result.head())
    return result, points


# # torque% to torque
# def torquePercent2torque(iterable, info):
#
#     def get_maxtorque(item, lst):
#         for list_aux in lst:
#             if (item[0] >= list_aux[1]) & (item[0] <= list_aux[2]):
#                 return item[-1] * (list_aux[3][0] * item[0] + list_aux[3][1])
#         else:
#             return 0
#
#     # construct modelName
#     pickleName = '_'.join([info['manufacturer'], info['model']])
#     picklePath = os.path.join('./instance/static', '%s.pickle' % pickleName)
#
#     with open(picklePath, "rb") as handle:
#         list_all = pickle.load(handle)
#     # 计算最大扭矩
#     result = [{'speed': i[0], 'torque': get_maxtorque(i, list_all) / 100} for i in iterable]
#     return result


# torque% to torque and  calculate oil
def torquePercent2torque(mappings, info):
    # construct params to predict
    p = {}
    p['picName'] = '_'.join([info['manufacturer'], info['model']])
    # p['data'] = [{'speed': i[0], 'torque(%)': i[-1]} for i in iterable]
    p['data'] = mappings
    from ..algorithm import predict
    output = predict(p, percent=True)
    print('ouput', len(output), output.head())
    output = list(output.loc[:, ['speed', 'torque']].T.to_dict().values())
    return output
