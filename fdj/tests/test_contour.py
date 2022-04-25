# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

"""
import unittest
import base64
import pandas as pd
from utils import req


class TestCommand(unittest.TestCase):

    def setUp(self) -> None:
        """
            method called setUp(), which the testing framework will automatically call for every single test we run:
        """
        pass

    def req(self, p, endPoint, files=None):
        self.assertEqual(req(p, endPoint, files), 0)

    # contour
    def testContourConstruct(self):
        # 加载负荷数据
        data = pd.read_excel('./static/375-6H-国三部分负荷.xlsx', engine='openpyxl')
        print('data', data.head())
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"data": list(data.T.to_dict().values())}
             }
        self.req(p, 'contour/generate')

    def testContourSave(self):
        # 加载负荷数据
        data = pd.read_excel('./static/375-6H-国三部分负荷.xlsx', engine='openpyxl')
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"model": "SY375H",
                                 "manufacturer": "五十铃",
                                 "picName": "test"},
                        "thres": {"rpm_min": 0,
                                  "rpm_max": 2000,
                                  "trq_min": 0,
                                  "trq_max": 2000},
                        "data": list(data.T.to_dict().values())
                        }
             }
        # png
        png = './instance/tmp/png/tmp_contour_test.png'
        with open(png, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            base64_data = str(base64_data, encoding='utf-8')
        self.req(p, 'contour/save', files=base64_data)

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass


# if __name__ == '__main__':
#
#     unittest.main()
