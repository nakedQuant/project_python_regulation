# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import numpy as np
import pandas as pd
import time
from instance.lib import rgb_numpy, rgb_memview, rgb_prange


def points(num):
    # x = np.random.choice(range(100, 200), 1000)
    # y = np.random.choice(range(30, 120), 1000)
    x = np.random.randint(700, 2000, num)
    y = np.random.randint(300, 1200, num)
    # out = np.zeros_like(x)
    z = np.array(list(zip(x, y)))
    # mappings
    m = [{'speed': i[0], 'torque': i[1]} for i in z]
    return m


def simulateRgb(output, r=50, threshold=1000):

    # 基于长度和阈值构建区间列表
    def thresInterval(length, threshold):
        start = range(length)[::threshold]
        end = range(length)[threshold::threshold]
        intervals = list(zip(start, end))
        # keep intervals complete
        bottom = (end[-1], length)
        intervals.append(bottom)
        return intervals

    def run(delta, df, delimeter):
        s, e = delta
        item = df.iloc[s: e, :]
        x = np.array(item['speed'].values)
        y = np.array(item['torque'].values)
        z = np.array(list(zip(x, y)))
        # nums = rgb_memview(r, np.array(list(z)))
        # nums = rgb_numpy(r, np.array(list(z)))
        nums = rgb_numpy(delimeter, z)
        # nums = rgb_prange(r, np.array(list(z)))
        # nums to rgbRate
        # nums = list(map(lambda x: 255 * x/sum(nums), nums))
        res = [{'speed': item[0][0], 'torque': item[0][1], 'color': item[1]} for item in zip(z, nums)]
        return res

    # mappings -> dataframe
    output = pd.DataFrame(output)
    print('simulateRgb', output.head())
    # astype
    output = output.astype(np.int32)
    # length = len(output)
    # slice
    intervals = thresInterval(len(output), threshold)
    print('intervals', intervals)

    from functools import partial
    func = partial(run, df=output, r=r**2)
    outcome = [func(args) for args in intervals]
    # outcome = [run(args) for args in intervals]
    # chain
    from itertools import chain
    result = list(chain(*outcome))
    return result


if __name__ == '__main__':

    t1 = time.time()
    num, r = (10325, 50)
    p = points(num)
    print('p length', len(p))
    # simulateRgb(p, r)
    positions = simulateRgb(p, r)
    print('rgb_numpy nums', len(positions), positions[:10])
    positions_1 = simulateRgb(p, 100)
    print('rgb_numpy nums_1', len(positions_1), positions_1[:10])
    positions_2 = simulateRgb(p, 50)
    print('rgb_numpy nums_2', len(positions_2), positions_2[:10])
    elapsed = time.time() - t1
    print('rgb_numpy elapsed', elapsed)
