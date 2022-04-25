# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import json
import pandas as pd
from sqlalchemy import select, and_
from ..utils import cf


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
