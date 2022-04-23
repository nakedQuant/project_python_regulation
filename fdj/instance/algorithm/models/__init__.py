# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import joblib
import os
import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsRegressor
from .predict import predict


# def generateModel(theory, model_name):
def generateModel(params):
    """
    根据转速和扭矩生成理论油耗计算模型，并将模型保存在当前路径下

    Parameters：
        theory - 训练数据，包括speed、torsion、oil三列，dataframe格式
        machine_type - 数据对应的机器型号，用于模型命名，str类型

    Returns：
        无
    """
    # tranform theory format
    # data = pd.DataFrame(params['data'])
    # data = pd.DataFrame(params.pop('data'))
    mappings = params.pop('data')
    data = pd.DataFrame(mappings['model'])
    # main logic
    data.rename(columns={'Rpm': 'speed', 'Nm': 'torque', 'g/Kwh': 'oil'}, inplace=True)
    model_name = params['picName']
    x_train = data[['speed', 'torque']]
    y_train = data['oil']
    dis_knr = KNeighborsRegressor(weights='distance')
    dis_knr.fit(x_train, y_train)
    # 构建并保存模型 --- 模型名称与图片名称一致
    p = os.path.join(os.path.abspath('./instance/algorithm/models'), '%s.model' % model_name)
    # joblib.dump(dis_knr, '{}.model'.format(model_name))
    joblib.dump(dis_knr, p)


def generatePickle(data, name):

    def get_linear_func(dct, file):
        vertex_aux = pd.DataFrame(dct)
        list_aux = []
        for i in range(len(vertex_aux)-1):
            x1 = vertex_aux['rmp'][i]
            y1 = vertex_aux['Nm'][i]
            x2 = vertex_aux['rmp'][i+1]
            y2 = vertex_aux['Nm'][i+1]
            a_aux = (y2 -y1) / (x2 - x1)
            b_aux = y1 - a_aux * x1
            list_aux.append([['l' + str(i)], x1, x2, [a_aux, b_aux]])
            with open(file, 'wb') as  handle:
                pickle.dump(list_aux, handle)

    # locate
    p = os.path.join(os.path.abspath('./instance/static'), '%s.pickle' % name)
    get_linear_func(data, p)
