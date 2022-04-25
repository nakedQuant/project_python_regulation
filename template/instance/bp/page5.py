# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

blueprint:万有特性曲线
"""
from flask import Blueprint
from ..utils import jsonEncoder


page5 = Blueprint('page5', __name__, url_prefix='/page5')


@page5.route('/index', methods=('Get',))
def index():
    resp = 'Hello, page5'
    return jsonEncoder(resp)
