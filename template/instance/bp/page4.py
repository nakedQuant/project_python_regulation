# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:动态匹配
"""
from flask import Blueprint
from ..utils import jsonEncoder


page4 = Blueprint('page4', __name__, url_prefix='/page4')


@page4.route('/index', methods=('Get',))
def index():
    resp = 'Hello, page4'
    return jsonEncoder(resp)
