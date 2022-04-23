# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import pickle
import joblib
import pandas as pd
import os

modelPath = os.path.abspath('./instance/static')


def get_maxtorque(rpm, lst):
    for list_aux in lst:
        if (rpm >= list_aux[1]) & (rpm <= list_aux[2]):
            return list_aux[3][0] * rpm + list_aux[3][1]


def _modify_df(df, model_name):
    """
    if model=="SY375":
        with open("D:\\ipyfiles\\universial_c\\SY375.pickle", "rb") as handle:
            list_all=pickle.load(handle)
    else:
        with open("SY485.pickle", "rb") as handle:
            list_all=pickle.load(handle)
    """
    pickleName = '_'.join(model_name.split('_')[:2])
    # print(("{}.pickle".format(model_name)))
    # with open("{}.pickle".format(model_name), "rb") as handle:
    picklePath = os.path.join(modelPath, '%s.pickle' % pickleName)

    with open(picklePath, "rb") as handle:
        list_all = pickle.load(handle)
    # 计算最大扭矩
    df.insert(loc=0, column="max_torque", value=df["speed"].apply(lambda x: get_maxtorque(x, lst=list_all)))
    # 不再范围需要设置为0
    df['max_torque'].fillna(0, inplace=True)
    return df


def modify_df(df):
    # df = _modify_df(df, model_name)
    # 计算实际扭矩
    df["torque"] = df["max_torque"] * df["torque(%)"]
    # df.insert(loc=0, column="torsion", value=df["max_torque"] * df["torsion(%)"])
    # 删除无用列
    del df['max_torque']
    return df


def predict(params, percent=False):
    """
    调用已有KNN模型进行理论油耗计算。

    Parameters：
        theory - DataFrame，原始数据；
        model_name - 模型名称，目前有五十铃_SY375,五十铃_SY485
        percent - bool，区分时扭矩百分比还是实际扭矩

    Returns：
        theory - DataFrame，原始数据+预测结果，增加一列['oil']

    Raises:
    """
    data = pd.DataFrame(params['data'])
    print('predict params', params)
    # process NaN
    data.fillna(0.0, inplace=True)
    modelName = params['picName']
    # 加载模型
    model = joblib.load(os.path.join(modelPath, '%s.model' % modelName))
    # max_torque
    data = _modify_df(data, modelName)
    if percent:
        # 根据扭矩百分比计算实际扭矩
        data['torque(%)'] = data['torque(%)'].apply(lambda x: float(x / 100))
        # data = modify_df(data, modelName)
        data = modify_df(data)
        # 理论油耗计算
        data['oil'] = model.predict(data[['speed', 'torque']])
        data['oil'] = data['oil'].apply(lambda x: round(x, 2))
        data['torque'] = data['torque'].apply(lambda x: int(x))
        # 将异常值替换为异常
        data['oil'][data['torque'] == 0] = '异常'
        data['torque'][data['torque'] == 0] = '异常'
    else:
        data['oil'] = model.predict(data[['speed', 'torque']])
        data['oil'] = data['oil'].apply(lambda x: round(x, 2))
    print('data', data.head())
    return data
