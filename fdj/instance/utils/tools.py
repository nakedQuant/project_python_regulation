# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import datetime
from functools import wraps
import base64
import json
import numpy as np
from typing import Any
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from .cfg import cf
# from ..lib import rgb_numpy, rgb_memview


def jsonEncoder(resp):

    class NpEncoder(json.JSONEncoder):

        def default(self, o: Any) -> Any:
            if isinstance(o, np.int):
                return int(o)
            elif isinstance(o, np.float):
                return float(o)
            elif isinstance(o, (np.array, np.ndarray)):
                return o.tolist()
            elif isinstance(o, pd.Timestamp):
                return o.strftime('%Y-%m-%d %H:%M:%S.%f')
            else:
                return super().default(o)

    return json.dumps(resp, ensure_ascii=False, indent=4, cls=NpEncoder)


def resample(f):
    """
    :param f: DataFrame
    :return: resample index
    """
    # 剔除重采样索引
    f = f[~f.index.duplicated(keep='last')]
    # 重采样
    # resm = f.resample(rule='0.05S').asfreq()[:]
    freq = cf.get('plot', 'resample')
    resam = f.resample(rule=freq).asfreq()[:]
    return resam.index


def aes_ecb_encrypt(raw, style='pkcs7'):
    """
    :param raw: string
    :return:
    """
    # str to bytes
    raw = raw if isinstance(raw, bytes) else raw.encode('utf-8')
    # AES.block_size == 16
    encrypted = cipher.encrypt(pad(raw, AES.block_size, style=style))
    utf8_encypted = base64.b64encode(encrypted).decode('utf-8')
    return utf8_encypted


def aes_ecb_decrypted(encrypted):
    try:
        # b64 = json.loads(encrypted)
        decryption = {}
        # for key, value in b64:
        for key, value in encrypted.items():
            value = base64.b64decode(value)
            value = unpad(cipher.decrypt(value), AES.block_size)
            decryption[key] = value.decode('utf-8')
    except json.JSONDecodeError:
        encrypted = base64.b64decode(encrypted)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        decrypted = decrypted.decode('utf-8')
    return decrypted


def _init_aes():
    secret = cf.get('service', 'secret')
    # length of key must be times of 16
    cipher = AES.new(secret.encode('utf-8'), AES.MODE_ECB)
    return cipher


# def simulateRgb(output, r=50, threshold=1000):
#
#     def run(delta, df, r):
#         s, e = delta
#         item = df.loc[s: e, :]
#         x = np.array(item['speed'].loc[s: e, ].values)
#         y = np.array(item['torque'].loc[s: e, ].values)
#         out = np.zeros_like(x)
#         z = np.array(list(zip(x, y)))
#         # nums = rgb_numpy(r, np.array(list(z)), out)
#         nums = rgb_memview(r, np.array(list(z)), out)
#         # nums to rgbRate
#         # rgb = list(map(lambda x: 255 * x/sum(nums), nums))
#         # rgb > 'rgb()'
#         # rgb = ['rgb(%d,%d,%d)' % (i, i, i) for i in rgb]
#         rgb = [r if r <= 255 else 255 for r in nums]
#         item.loc[:, 'color'] = rgb
#         res = list(item.T.to_dict().values())
#         # print('res', res[:5])
#         return res
#
#     # mappings -> dataframe
#     output = pd.DataFrame(output)
#     print('simulateRgb', output.head())
#     # astype
#     output = output.astype('int')
#     length = len(output)
#     # slice
#     start = range(length)[::threshold]
#     end = range(length)[threshold::threshold]
#     intervals = list(zip(start, end))
#     # keep intervals complete
#     if length % threshold:
#         from itertools import chain
#         last = (end[-1], length)
#         intervals.append(last)
#
#     from functools import partial
#     func = partial(run, df=output, r=r**2)
#     outcome = [func(args) for args in intervals]
#     # outcome = [run(args) for args in intervals]
#     # chain
#     result = list(chain(*outcome))
#     return result


# def simulateRgb(output, r=50, threshold=1000):
#
#     def run(delta, df, r):
#         s, e = delta
#         item = df.loc[s: e, :]
#         x = np.array(item['speed'].loc[s: e, ].values)
#         y = np.array(item['torque'].loc[s: e, ].values)
#         out = np.zeros_like(x)
#         z = np.array(list(zip(x, y)))
#         # memory leak heap
#         # nums = rgb_numpy(r, np.array(list(z)), out)
#         nums = rgb_memview(r, np.array(list(z)), out)
#         # nums to rgbRate
#         # rgb = list(map(lambda x: 255 * x/sum(nums), nums))
#         # rgb > 'rgb()'
#         # rgb = ['rgb(%d,%d,%d)' % (i, i, i) for i in rgb]
#         rgb = [r if r <= 255 else 255 for r in nums]
#         item.loc[:, 'color'] = rgb
#         res = list(item.T.to_dict().values())
#         # print('res', res[:5])
#         return res
#
#     # mappings -> dataframe
#     output = pd.DataFrame(output)
#     output = output.astype('int')
#     length = len(output)
#     # slice intervals
#     start = range(length)[::threshold]
#     end = range(length)[threshold::threshold]
#     intervals = list(zip(start, end))
#     # keep intervals complete
#     if length % threshold:
#         from itertools import chain
#         last = (end[-1], length)
#         intervals.append(last)
#
#     # partial
#     from functools import partial
#     func = partial(run, df=output, r=r**2)
#
#     # parallel
#     from multiprocessing import cpu_count
#     from concurrent.futures.thread import ThreadPoolExecutor
#     from concurrent.futures import as_completed
#     # 1、多进程开销太大超过的可以节省的时间,多线程开销比循环慢，
#     # 2、主要是通过cython编译与内存试图数据结构在1000-3000单次就非常快,循环没有过大开销，如果超过总点数很大，选择方案1
#     # from concurrent.futures.process import ProcessPoolExecutor
#     # with ProcessPoolExecutor(max_workers=cpu_count()) as p:
#     with ThreadPoolExecutor(max_workers=cpu_count()) as p:
#         futures = [p.submit(func, args) for args in intervals]
#
#     # get result
#     outcome = [f.result() for f in as_completed(futures)]
#     # chain
#     from itertools import chain
#     result = list(chain(*outcome))
#     print('result', result[:3])
#     return result

def count_time(f):
    func = f.__name__
    init = datetime.datetime.now()

    @wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        elapsed = datetime.datetime.now() - init
        print(f'{func} {elapsed.seconds}')
        return res
    return wrapper


def uniqueName(info):
    # 构建唯一版本描述
    tag = '_'.join([info, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    return tag


cipher = _init_aes()
