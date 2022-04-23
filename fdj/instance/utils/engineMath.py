# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import numpy as np
import pandas as pd


def parseTheory(data):
    """
        泵输入扭矩 = 泵输出扭矩 / 0.85
        液压功率 = 转速 * 泵输出扭矩  / 9549
        发动机输出功率 = 液压功率 / 0.85
        发动机总输出功率 = 发动机输出功率 + 附件功率
    """
    Cols = {'brake': int, 'speed': int, 'torque_out': int, 'appendix_power': int, 'hOil': float}
    # calculate
    frame = pd.DataFrame(data)
    frame = frame.astype(Cols)
    # frame['brake'] = frame['brake'].astype('int')
    # frame['speed'] = frame['speed'].astype('int')
    # frame['torque_out'] = frame['torque_out'].astype('int')
    frame.loc[:, 'torque'] = round(frame['torque_out'] / 0.85, 2)
    frame.loc[:, 'hydraulic_power'] = round(frame['speed'] * frame['torque_out'] / 9549, 2)
    frame['engine_power'] = round(frame['hydraulic_power'] / 0.85)
    frame['engine_full_power'] = round(frame['engine_power'] + frame['appendix_power'], 2)
    mappings = list(frame.T.to_dict().values())
    return mappings


def engineProperty(data):
    """
      1、发动机外特性扭矩（万有特性曲线上线） ---- 基于模型得出
      2、发动机外特性功率 = 转速 * 发动机外特性扭矩 / 9549
      3、匹配饱和度 = 泵输入扭矩 / 发动机外特性扭矩
      4、理论小时油耗（L / h ) = 理论油耗比值 * 发动机总输入功率 / 850
      5、修正系数 = 理论小时油耗 / 实际小时油耗
    """
    # 外特性特征
    data['engine_property_torque'] = data['max_torque']
    data['engine_property_power'] = data.apply(lambda x: round(x['speed'] * x['engine_property_torque'] / 9549, 2),
                                               axis=1)
    #
    saturation = data.apply(lambda x: round(x['torque'] / x['engine_property_torque'], 2), axis=1)
    data['saturation'] = np.nan_to_num(saturation, posinf=0.0, neginf=0.0)
    data['theory_hOil'] = data.apply(lambda x: round(x['oil'] * x['engine_full_power'] / 850, 2), axis=1)
    data['revise'] = data.apply(lambda x: round(x['theory_hOil'] / x['hOil'], 2), axis=1)
    return data
