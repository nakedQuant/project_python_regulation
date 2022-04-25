# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:曲线对比

"""
from flask import Blueprint
from ..utils import jsonEncoder


page1 = Blueprint('page1', __name__, url_prefix='/page1')


@page1.route('/index', methods=('Get',))
def index():
    resp = 'Hello, page1'
    return jsonEncoder(resp)
