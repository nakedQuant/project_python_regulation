# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import subprocess
from instance.db import dbs, DB
from instance.utils import cf, overwrite

# 初始化主表
params = [{"model": "SY375H", "manufacturer": "五十铃"},
          {"model": "485", "manufacturer": "五十铃"},
          {"model": "375IDS", "manufacturer": "康明斯L9"}]


def run():
    if cf.get('property', 'initialize') == 'True':
        DB._reset(params)
        cf.set('property', 'initialize', 'False')
    if cf.get('property', 'truncate') == 'True':
        dbs._truncate(params)
        cf.set('property', 'truncate', 'False')
    # rewrite ini
    overwrite(cf, 'conf.ini')
    # gunicorn
    # subprocess.Popen('nohup gunicorn -c gunicorn.conf.py service:app &')
    subprocess.run(['nohup', 'gunicorn', '-c', 'gunicorn.conf.py', 'service:app', '&'])


if __name__ == '__main__':

    run()
