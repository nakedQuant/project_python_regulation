# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import os
import configparser

cf = configparser.ConfigParser()
cur_dir = os.path.abspath('.')  # 获取当前文件所在目录


def readConfig(name):
    configpath = os.path.join(cur_dir, name)
    cf.read(configpath)  # 读取配置文件
    return cf


def overwrite(cf, name):
    configpath = os.path.join(cur_dir, name)
    with open(configpath, 'r+') as f:
        cf.write(f)


cf = readConfig('conf.ini')
