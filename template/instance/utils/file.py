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


def extConf(fPath):
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
    frame = pd.DataFrame(cache)
    frame.dropna(how='any', inplace=True)
    frame.sort_values(by='figure', inplace=True)
    # frame = pd.read_excel(file, engine='openpyxl')
    return frame


def whereis(directory, pattern):
    """
    :param directory: str
    :param pattern: str
    :return: []
    """
    files = glob.glob(os.path.join(directory, pattern), recursive=True)
    return files
