# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import os
import pandas as pd
import glob
import re

savePath = os.path.abspath('./instance/tmp/history')


Cols = {'档位': 'brake', '转速': 'speed', '泵输出扭矩': 'torque_out',
        '泵输入扭矩': "torque", "液压功率": "hydraulic_power",
        "泵最大扭矩": "torque_max", "发动机输出功率": "engine_power",
        "发动机总输出功率": "engine_full_power", "附件功率": "appendix_power",
        "发动机外特性扭矩": "engine_property_torque", "发动机外特性功率": "engine_property_power",
        "匹配饱和度": "saturation", "理论油耗比值": "oil", "理论小时油耗": "theory_hOil",
        "实际小时油耗": "hOil", "修正系数": "revise"}


def read(file):
    """
    :param file: filePath
    :return: DataFrame
    """
    # 解析Excel或者csv文件
    if file.endswith('csv'):
        with open(file, 'r') as f:
            data = []
            for r in f.readlines():
                raw = r.split(',')
                raw = [item.strip() for item in raw]
                data.append(raw)
        frame = pd.DataFrame(data[1:], columns=data[0])
    else:
        frame = pd.read_excel(file, engine='openpyxl')
    return frame


def extExcel(p):
    # 解析档位的Excel表格
    """
    :param p: path
    :return: DataFrame
    """
    frame = read(p)
    # rename
    frame.rename(columns=Cols, inplace=True)
    # brake into integer
    frame['brake'] = frame['brake'].astype(int)
    frame['speed'] = frame['speed'].astype(int)
    frame['torque_out'] = frame['torque_out'].astype(int)
    frame['torque_max'] = frame['torque_max'].astype(int)
    frame['appendix_power'] = frame['appendix_power'].astype(int)
    frame['hOil'] = frame['hOil'].astype(float)
    return frame


def extConf(fPath):
    # 解析配置文件
    """
    :param fPath: str
    :return: DataFrame
    """
    # \s 匹配空白字符
    pattern = r'(\s)+'
    cache = []
    with open(fPath, 'r') as f:
        for r in f.readlines():
            sep = re.sub(pattern, ' ', r)
            cache.append(sep.split(' ')[:-1])
    # concat
    frame = pd.DataFrame(cache, columns=['En', 'can', 'loc', 'Ch', 'figure', 'subplots'])
    frame.dropna(how='any', inplace=True)
    frame.sort_values(by='figure', inplace=True)
    return frame


def whereis(token, name, category):
    # 根据token与文件名判断数据数据源或者配置文件是否存在
    """
    :param token: str
    :param name: str
    :param category: source or conf
    :return: []
    """
    pattern = '%s_%s' % (token, name)
    directory = os.path.join(savePath, category)
    files = glob.glob(os.path.join(directory, pattern), recursive=True)
    return files
