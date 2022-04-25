# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:静态匹配
"""
from flask import Blueprint
from ..utils import jsonEncoder


page2 = Blueprint('page2', __name__, url_prefix='/page2')


@page2.route('/index', methods=('Get',))
def index():
    resp = 'Hello, page2'
    return jsonEncoder(resp)
