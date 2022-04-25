# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

"""
import unittest
from utils import req


class TestCommand(unittest.TestCase):

    def setUp(self) -> None:
        """
            method called setUp(), which the testing framework will automatically call for every single test we run:
        """
        pass

    def req(self, p, endPoint, files=None):
        self.assertEqual(req(p, endPoint, files), 0)

    # analyze
    def testAnalyzeCalculate(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"model1": {"picName": "五十铃_SY375H"},
                                 "model2": {"picName": "五十铃_485"}},
                        "data": [{"brake": 1, "speed": 1000, "torque": 1500},
                                 {"brake": 2, "speed": 1100, "torque": 1600},
                                 {"brake": 3, "speed": 1200, "torque": 1700},
                                 {"brake": 4, "speed": 1300, "torque": 1800}
                                 ]
                        }
             }
        self.req(p, 'analyze/calculate')

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass


# if __name__ == '__main__':
#
#     unittest.main()
