# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:历史结果分析
"""
from flask import Blueprint
from ..utils import jsonEncoder


page3 = Blueprint('page3', __name__, url_prefix='/page3')


@page3.route('/index', methods=('Get',))
def index():
    resp = 'Hello, page3'
    return jsonEncoder(resp)
