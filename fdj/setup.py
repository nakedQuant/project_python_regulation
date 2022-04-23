# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import numpy as np
from setuptools import setup
from Cython.Build import cythonize

setup(
    #name='rgb',
    ext_modules=cythonize(['./instance/lib/*.pyx']),
    include_dirs=[np.get_include()],
    zip_safe=False
)
