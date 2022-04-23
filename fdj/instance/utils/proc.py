# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import os
from functools import lru_cache, partial
from .cfg import cf
from .can import universe_parse
from .file import read, whereis, extConf
from .tools import resample


def figureLines(params):
    # 基于figure解析数据源与配置文件获取对应的序列
    """
    :param params: {"figure": 1, "source": "test", "conf": "test"}
    :return: list
    """
    figure = params.pop('figure')
    # retrieve data
    f1, f2 = fetch(**params)
    # reformat conf index
    conf = f2[f2['figure'] == figure]
    conf.index = range(len(conf))
    # 重采样 索引
    index = resample(f1)
    freeze = partial(sub_plot, conf=conf, f1=f1, index=index)
    # parallel
    # # 通过gunicorn 本身就是多进程、多线程，如果在内部函数中实现多进程就会卡住
    # from multiprocessing import Pool
    # with Pool(processes=os.cpu_count()) as p:
    #     pool = [p.apply_async(freeze, subplot)
    #             for subplot in conf['subplots'].unique()]
    #     result = [f.get() for f in pool]
    from concurrent.futures import ThreadPoolExecutor
    from concurrent.futures import as_completed
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
          futures = [executor.submit(freeze, subplot) for subplot in conf['subplots'].unique()]
    result = [f.result() for f in as_completed(futures)]
    return result


@lru_cache(maxsize=128)
def fetch(token, source, conf):
    #  获取source and conf 由于lru_cache --- 参数必须可以hashable [key]
    """
    :param token: str
    :return: tuple
    """
    source = whereis(token, source, 'source')
    # print('source', source)
    f1 = read(source[0])
    f1 = f1.loc[:, ['WRITE_TIME', 'MAKE_CAN_ID(HEX)', 'DATA(HEX)']]
    f1.index = f1['WRITE_TIME'].apply(lambda x: x[1:-1])
    f1.sort_index(ascending=True, inplace=True)
    print('f1', f1.head())
    # 配置文件
    # conf = whereis(token, params['conf'], 'conf')
    conf = whereis(token, conf, 'conf')
    f2 = extConf(conf[0])
    print('f2', f2.head())
    return f1.iloc[:, 1:], f2


def sub_plot(subplot, conf, f1, index):
    output = {'subplot': subplot, 'data': []}
    # UserWarning: DataFrame columns are not unique, some columns will be omitted. .T --- index unique
    for item in conf[conf['subplots'] == subplot].T.to_dict().values():
        temp = {}
        data = f1[f1['MAKE_CAN_ID(HEX)'] == item['can']]['DATA(HEX)']
        v = data.apply(lambda x: universe_parse(x, item['loc']))
        # series reindex
        v = v.reindex(index)
        v.fillna(method='ffill', inplace=True)
        v.fillna(method='bfill', inplace=True)
        v.fillna(0, inplace=True)
        v.sort_index(ascending=True, inplace=True)
        temp['data'] = v.values.tolist()
        temp['name'] = item['Ch']
        temp['type'] = cf.get('plot', 'type')
        temp['sampling'] = cf.get('plot', 'sampling')
        output['data'].append(temp)
        return output


def formatOutput(frame):
    # 按照约定格式转换planName与planVersion
    """
    :param frame: DataFrame
    :return: []dict
    """
    r = frame.groupby('planName').apply(lambda x: x.to_dict())
    r = r.values.tolist()
    # print('r', type(r), r)

    def func(item):
        mappings = {}
        mappings['planName'] = list(item['planName'].values())[0]
        version = [{'planVersion': v} for v in item['planVersion'].values()]
        mappings['theory'] = version
        return mappings

    output = [func(item) for item in r]
    return {'plan': output}
