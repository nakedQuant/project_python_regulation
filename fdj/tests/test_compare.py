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

    # compare
    def testCompareCalculate(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"picName": "五十铃_SY375H"},
                        "data": [{"time": "2021-11-30 19:55:12.490", "speed": 1000, "torque(%)": 0.65},
                                 {"time": "2021-11-30 19:56:12.515", "speed": 1100, "torque(%)": 0.69},
                                 {"time": "2021-11-30 19:57:12.523", "speed": 1200, "torque(%)": 0.72},
                                 {"time": "2021-11-30 19:58:12.530", "speed": 1300, "torque(%)": 0.79}
                                 ]
                        }
             }
        self.req(p, 'compare/calculate')

    def testCompareSave(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"model": "SY375H",
                                 "manufacturer": "五十铃",
                                 "matchPlan": "第二次测试"},
                        "data": [{"time": "2021-11-30 19:56:12.490", "speed": 1000, "torque(%)": 0.65,
                                  "cumOil": 6, "oilFlow": 0.5},
                                 {"time": "2021-11-30 19:57:12.510", "speed": 2000, "torque(%)": 0.72,
                                  "cumOil": 7, "oilFlow": 0.6},
                                 {"time": "2021-11-30 19:58:12.530", "speed": 3000, "torque(%)": 0.85,
                                  "cumOil": 8, "oilFlow": 0.7}]
                        }
             }
        self.req(p, 'compare/save')

    def testCompareGetPlans(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"model": "SY375H", "manufacturer": "五十铃"}
                        }
             }
        self.req(p, 'compare/getPlans')

    def testComparePlanLoad(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"matchPlan": "第二次测试_2022-02-15 14:38:20.274902"}
                        }
             }
        self.req(p, 'compare/planLoad')

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass


# if __name__ == '__main__':
#
#     unittest.main()
