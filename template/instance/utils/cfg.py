# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import os
import configparser
from pathlib import Path

cf = configparser.ConfigParser()

cur_dir = str(Path(__file__).resolve().parent.parent)


def readConfig(name):
    p = os.path.join(cur_dir, name)
    print('configpath', p)
    cf.read(p)  # 读取配置文件
    return cf


def overwrite(cf, name):
    p = os.path.join(cur_dir, name)
    with open(p, 'r+') as f:
        cf.write(f)


cf = readConfig('conf.ini')
