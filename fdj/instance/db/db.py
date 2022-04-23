# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import json
import pandas as pd
from sqlalchemy import select, and_
from ..utils import cf, uniqueName


class DB(object):

    _cache = {}

    def __new__(cls):
        if 'instance' not in cls._cache:
            print('__new__')
            from .models import initialize_meta
            p = initialize_meta()
            instance = super().__new__(cls)
            for k, v in p.items():
                setattr(instance, k, v)
            # setattr table name
            for tbl, obj in p['metadata'].tables.items():
                setattr(instance, tbl, obj)
            cls._cache['instance'] = instance
        return cls._cache['instance']

    def __init__(self):
        self.bulk = cf.getint('property', 'bulk')

    def _load_bluks(self, sql):
        # 从数据库加载数据
        while True:
            try:
                with self.engine.connect() as con:
                    output = con.execute(sql).fetchall()
                    break
            except Exception as e:
                print(e)
                pass
        return output

    def _dump_bluks(self, sql, params):
        # 分批次入库
        if not isinstance(params, (list, dict)):
            raise TypeError
        with self.engine.begin() as con:
            if isinstance(params, dict):
                con.execute(sql, params)
            else:
                count = len(params) // self.bulk + 1
                for c in range(count):
                    con.execute(sql, params[c * self.bulk: (c + 1) * self.bulk])

    def add_engines(self, param):
        # 添加发动机种类
        self._dump_bluks(self.category.insert(), param)

    def retrieve_engines(self):
        # 获取发动机信息
        sql = select([self.category.c.model, self.category.c.manufacturer])
        frame = pd.DataFrame(self._load_bluks(sql), columns=['model', 'manufacturer'])
        return frame

    def add_picNames(self, params):
        # 添加发动机万有引力曲线名称
        self._dump_bluks(self.pic.insert(), params)

    def retreive_picThres(self, params):
        picName = params['info']['picName']
        sql = select([self.pic.c.rpm_max, self.pic.c.rpm_min, self.pic.c.trq_max, self.pic.c.trq_min]).\
            where(self.pic.c.picName == picName)
        frame = pd.DataFrame(self._load_bluks(sql), columns=['rpm_max', 'rpm_min', 'trq_max', 'trq_min'])
        return frame.iloc[0, :].to_dict()

    def retrieve_picNames(self, params):
        """
            获取发动机万有引力曲线图片名称
        """
        info = params['info']
        model = info['model']
        manufacturer = info['manufacturer']
        # execute
        sql = select([self.pic.c.picName]).where(
            and_(self.pic.c.model == model, self.pic.c.manufacturer == manufacturer)
        )
        result = [r[0] for r in self._load_bluks(sql)]
        return result

    def add_planNames(self, params):
        # 增加方案名称
        """
            input: params dict
                            {'model': '375,
                             'manufacturer': '五十铃',
                             'picName': 'test',
                             'planName': '1',
                             'planVersion': 'test'}
            return:
                0
        """
        self._dump_bluks(self.planName.insert(), params)

    def retrieve_planNames(self, params):
        # 获取理论油耗方案名称
        info = params['info']
        model = info['model']
        manufacturer = info['manufacturer']
        sql = select([self.planName.c.planName, self.planName.c.planVersion]).where(
            and_(self.planName.c.model == model, self.planName.c.manufacturer == manufacturer)
        )
        frame = pd.DataFrame(self._load_bluks(sql), columns=['planName', 'planVersion'])
        return frame

    def retrieve_plans(self, params):
        # 获取理论油耗方案数据
        version = params['info']['planVersion']
        sql1 = select([self.plan.c.brake, self.plan.c.speed, self.plan.c.torque, self.plan.c.torque_out,
                       self.plan.c.torque_max, self.plan.c.hydraulic_power, self.plan.c.engine_power,
                       self.plan.c.engine_property_power, self.plan.c.engine_full_power, self.plan.c.appendix_power,
                       self.plan.c.engine_property_torque, self.plan.c.saturation, self.plan.c.oil,
                       self.plan.c.theory_hOil, self.plan.c.hOil, self.plan.c.revise]).\
            where(self.plan.c.planVersion == version)
        # data
        frame = pd.DataFrame(self._load_bluks(sql1),
                             columns=['brake', 'speed', 'torque', 'torque_out', 'torque_max', 'hydraulic_power',
                                      'engine_power', 'engine_property_power', 'engine_full_power', 'appendix_power',
                                      'engine_property_torque', 'saturation', 'oil', 'theory_hOil', 'hOil', 'revise'])
        frame = frame.astype()
        # picName --- 图片名称如果是原始图片则为空
        sql2 = select([self.planName.c.picName]).where(self.planName.c.planVersion == version)
        res = self._load_bluks(sql2)[0][0]
        # pic = '' if len(res.split('_')) == 2 else res
        pic = res if res else ''
        # output
        output = {'data': list(frame.T.to_dict().values()), 'info': pic}
        return output

    def save_plans(self, params):
        # 保存理论油耗计算方案
        info = params['info']
        # unique
        # info['planVersion'] = self.attach(info['planVersion'])
        info['planVersion'] = uniqueName(info['planVersion'])
        with self.engine.begin() as con:
            # 保存方案名称
            con.execute(self.planName.insert(), [info])
            # 保存planData
            for item in params['data']:
                item.update({'planVersion': info['planVersion']})
            con.execute(self.plan.insert(), params['data'])

    def add_matchPlan(self, params):
        # 保存动态多点匹配
        self._dump_bluks(self.matchName.insert(), [params['info']])

    def retrieve_matchplanNames(self, params):
        # 获取多点动态匹配方案名称
        model = params['info']['model']
        manufacturer = params['info']['manufacturer']
        # execute
        sql = select([self.matchName.c.planName]).where(
            and_(self.matchName.c.model == model, self.matchName.c.manufacturer == manufacturer)
        )
        result = [r[0] for r in self._load_bluks(sql)]
        return result

    def retrieve_matchplans(self, params):
        # 获取多点动态匹配方案
        match = params['info']['matchPlan']
        sql1 = select([self.matchPlan.c.time, self.matchPlan.c.speed, self.matchPlan.c.torquePercent,
                       self.matchPlan.c.torque, self.matchPlan.c.oil, self.matchPlan.c.cumOil, self.matchPlan.c.oilFlow])\
            .where(self.matchPlan.c.planName == match)
        f1 = pd.DataFrame(self._load_bluks(sql1), columns=['time', 'speed', 'torque(%)', 'torque',
                                                           'oil', 'cumOil', 'oilFlow'])
        # print('f1', f1.head())
        # 获取对应的机型
        sql2 = select([self.matchName.c.model, self.matchName.c.manufacturer, self.matchName.c.points]).\
            where(self.matchName.c.planName == match)
        f2 = pd.DataFrame(self._load_bluks(sql2), columns=['model', 'manufacturer', 'points'])
        # 获取打点值
        points = f2.pop('points')
        # print('f2', f2.head())
        output = {'data': list(f1.T.to_dict().values()), 'info': f2.iloc[0, :].to_dict(),
                  'points': json.loads(points.values[0])}
        return output

    def save_matchplans(self, params):
        # 保存多点动态匹配方案
        with self.engine.begin() as con:
            info = params['info']
            # unique
            # info['planName'] = self.attach(info['matchPlan'])
            info['planName'] = uniqueName(info['matchPlan'])
            # List[List] to str
            info['points'] = json.dumps(params['points'])
            # 保存匹配方案
            con.execute(self.matchName.insert(), info)
            for item in params['data']:
                item.update({'planName': info['planName']})
                item.update({'torquePercent': item['torque(%)']})
            # 保存方案数据
            con.execute(self.matchPlan.insert(), params['data'])

    def _truncate(self, params):
        with self.engine.begin() as con:
            for tbl in self.metadata.tables.values():
                con.execute(tbl.delete())
        # update primary table
        self.add_engines(params)

    @classmethod
    def _reset(cls, params):
        from .models import initialize_meta
        mappings = initialize_meta()
        mappings['metadata'].drop_all(bind=mappings['engine'])
        cls._cache.clear()
        # instance = super().__new__(DB)
        instance = DB()
        # update primary table
        instance.add_engines(params)

    def atexit(self):
        # Dispose of the connection pool used by this Engine
        self.engine.engine.dispose()

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.con.close()


def initialize_database():
    db = DB()
    return db
