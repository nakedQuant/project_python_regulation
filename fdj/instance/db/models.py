# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from ..utils import cf


def _initialize_engine():
    username = cf.get('development', 'username')
    password = cf.get('development', 'password')
    host = cf.get('development', 'host')
    port = cf.getint('property', 'port')
    db = cf.get('property', 'db')
    charset = cf.get('property', 'charset')
    pool_size = cf.getint('property', 'pool_size')
    max_overflow = cf.getint('property', 'max_overflow')

    # urllib.parse.quote_plus("kx%jj5/g")
    password = quote_plus(password)
    url = 'mysql+pymysql://{username}:{password}@{host}:{port}'.format(
        username=username,
        password=password,
        host=host,
        port=port)
    engine = create_engine(url, pool_size=pool_size, max_overflow=max_overflow)
    create_str = 'create database if not exists %s' % db
    engine.execute(create_str)
    # url db
    # engine = create_async_engine("mysql+aiomysql://user:pass@hostname/dbname?charset=utf8mb4")
    url_db = '{url}/{db}?charset={charset}'.format(url=url, db=db, charset=charset)
    # print('url_db', url_db)
    engine = create_engine(url_db, pool_size=pool_size, max_overflow=max_overflow)
    # engine.execute('use %s' % db)
    return engine


def initialize_meta():
    # metadata 初始化之后metadata.tables固定了
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们, import --- 执行脚本
    # scoped_session 线程安全
    # from sqlalchemy.orm import sessionmaker, scoped_session
    # db_session = scoped_session(sessionmaker(autocommit=False,
    #                                          autoflush=False,
    #                                          bind=engine))
    # from sqlalchemy.ext.declarative import declarative_base
    # Base = declarative_base()
    # Base.query = db_session.query_property()
    # Base.metadata.create_all(bind=engine)
    # from . import models
    # metadata.create_all(bind=engine, checkfirst=True)
    eng = _initialize_engine()
    # metadata = MetaData(bind=eng)
    metadata = MetaData()
    metadata.reflect(bind=eng)
    print('initialize_meta', len(metadata.tables))
    if not metadata.tables:
        # 发动机类型表
        category = sa.Table(
            'category',
            metadata,
            sa.Column(
                'id',
                sa.Integer,
                primary_key=True,
                autoincrement=True,
                index=True,
            ),
            sa.Column(
                'model',
                sa.String(50),
                nullable=False,
                unique=True,
                primary_key=True
            ),
            sa.Column(
                'manufacturer',
                sa.String(50),
                nullable=False,
            ),
            extend_existing=True
        )
        # 发动机对应的万有引力曲线图
        pic = sa.Table(
            'pic',
            metadata,
            sa.Column(
                'id',
                sa.Integer,
                primary_key=True,
                autoincrement=True,
                index=True,
            ),
            sa.Column(
                'model',
                sa.String(50),
                sa.ForeignKey(category.c.model, onupdate='CASCADE', ondelete='CASCADE'),
                nullable=False,
            ),
            sa.Column(
                'manufacturer',
                sa.String(50),
                nullable=False,
            ),
            sa.Column(
                'picName',
                sa.String(200),
                nullable=False,
                primary_key=True
            ),
            sa.Column(
                'rpm_min',
                sa.String(10),
                nullable=False,
            ),
            sa.Column(
                'rpm_max',
                sa.String(10),
                nullable=False,
            ),
            sa.Column(
                'trq_min',
                sa.String(10),
                nullable=False,
            ),
            sa.Column(
                'trq_max',
                sa.String(10),
                nullable=False,
            ),
            extend_existing=True
        )

        # 理论油耗计算方案
        planName = sa.Table(
            'planName',
            metadata,
            sa.Column(
                'id',
                sa.Integer,
                primary_key=True,
                autoincrement=True,
                index=True,
            ),
            # 机器类型
            sa.Column(
                'model',
                sa.String(50),
                sa.ForeignKey(category.c.model, onupdate='CASCADE', ondelete='CASCADE'),
                nullable=False,
            ),
            sa.Column(
                'manufacturer',
                sa.String(50),
                nullable=False,
            ),
            sa.Column(
                'picName',
                sa.String(50),
                nullable=False,
            ),
            # 方案名称
            sa.Column(
                'planName',
                sa.String(100),
                primary_key=True,
                nullable=False,
            ),
            # 方案版本
            sa.Column(
                'planVersion',
                sa.String(100),
                primary_key=True,
                nullable=False,
                unique=True
            ),
            extend_existing=True
        )

        # 理论油耗计算对应的方案
        plan = sa.Table(
            'plan',
            metadata,
            sa.Column(
                'id',
                sa.Integer,
                primary_key=True,
                autoincrement=True,
                index=True,
            ),
            # 方案版本
            sa.Column(
                'planVersion',
                sa.String(100),
                sa.ForeignKey(planName.c.planVersion, onupdate='CASCADE', ondelete='CASCADE'),
                primary_key=True,
                nullable=False
            ),
            sa.Column(
                'brake',
                sa.Integer,
                nullable=False,
                primary_key=True,
            ),
            sa.Column(
                'speed',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'torque_out',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'torque',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'torque_max',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'hydraulic_power',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'engine_power',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'engine_full_power',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'appendix_power',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'engine_property_torque',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'engine_property_power',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'saturation',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'oil',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'theory_hOil',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'hOil',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'revise',
                sa.Integer,
                nullable=False,
            ),
            extend_existing=True
        )

        # 动态多点匹配的方案
        matchName = sa.Table(
            'matchName',
            metadata,
            sa.Column(
                'id',
                sa.Integer,
                primary_key=True,
                autoincrement=True,
                index=True,
            ),
            sa.Column(
                'model',
                sa.String(50),
                sa.ForeignKey(category.c.model, onupdate='CASCADE', ondelete='CASCADE'),
                nullable=False,
            ),
            sa.Column(
                'manufacturer',
                sa.String(50),
                nullable=False,
            ),
            sa.Column(
                'planName',
                sa.String(100),
                primary_key=True,
                nullable=False,
                unique=True
            ),
            sa.Column(
                'points',
                sa.JSON,
                nullable=False
            ),
            extend_existing=True
        )

        # 动态多点匹配的方案
        matchPlan = sa.Table(
            'matchPlan',
            metadata,
            sa.Column(
                'id',
                sa.Integer,
                primary_key=True,
                autoincrement=True,
                index=True,
            ),
            sa.Column(
                'planName',
                sa.String(100),
                sa.ForeignKey(matchName.c.planName, onupdate='CASCADE', ondelete='CASCADE'),
                primary_key=True,
                nullable=False,
            ),
            sa.Column(
                'time',
                sa.String(50),
                primary_key=True,
                nullable=False
            ),
            sa.Column(
                'speed',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'torquePercent',
                sa.Float,
                nullable=False,
            ),
            sa.Column(
                'torque',
                sa.Integer,
                nullable=False,
            ),
            sa.Column(
                'oil',
                sa.Float,
                nullable=False,
            ),
            sa.Column(
                'cumOil',
                sa.Float,
                nullable=False,
            ),
            sa.Column(
                'oilFlow',
                sa.Float,
                nullable=False,
            ),
            extend_existing=True
        )

        # 版本信息
        appInfo = sa.Table(
            'appInfo',
            metadata,
            sa.Column(
                'id',
                sa.Integer,
                primary_key=True,
                autoincrement=True,
                index=True
            ),
            sa.Column(
                'appVersion',
                sa.String(255),
                primary_key=True,
                nullable=False,
            ),
            sa.Column(
                'updateTime',
                sa.DateTime,
                server_default=func.now(),
                # onupdate=func.now()
            ),
            # This constraint ensures a single entry in this table
            # sa.CheckConstraint('id >= 1'),
            extend_existing=True
        )
        metadata.create_all(bind=eng, checkfirst=True)
        metadata.reflect(bind=eng)
    # return metadata, engine
    return {'metadata': metadata, 'engine': eng}
