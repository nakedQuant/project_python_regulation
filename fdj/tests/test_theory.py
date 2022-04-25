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

    # # theory
    def testCalculate(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"picName": "五十铃_SY375H"},
                        "data": [{"brake": 1, "speed": 1000, "torque_out": 1400, "appendix_power": 100, "hOil": 32},
                                 {"brake": 2, "speed": 1200, "torque_out": 1500, "appendix_power": 105, "hOil": 33},
                                 {"brake": 3, "speed": 1300, "torque_out": 1600, "appendix_power": 107, "hOil": 34},
                                 {"brake": 4, "speed": 1400, "torque_out": 1700, "appendix_power": 115, "hOil": 35},
                                 {"brake": 5, "speed": 1500, "torque_out": 1800, "appendix_power": 117, "hOil": 36},
                                 {"brake": 6, "speed": 1600, "torque_out": 1900, "appendix_power": 118, "hOil": 37},
                                 {"brake": 7, "speed": 1700, "torque_out": 2000, "appendix_power": 120, "hOil": 38},
                                 {"brake": 8, "speed": 1800, "torque_out": 2100, "appendix_power": 130, "hOil": 39},
                                 {"brake": 9, "speed": 1900, "torque_out": 2200, "appendix_power": 140, "hOil": 41}
                                 ]
                        }
             }
        self.req(p, 'theory/calculate')

    def testSave(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"model": "SY375H", "manufacturer": "五十铃", "picName": "test",
                                 "planName": "1", "planVersion": "v0.1.2"},
                        "data": [{"brake": 1, "speed": 1300, "torque_out": 1100, "torque": 1200, "torque_max": 1300,
                                  "hydraulic_power": 2500, "engine_power": 2100, "engine_full_power": 2600,
                                  "appendix_power": 500, "engine_property_torque": 1400, "engine_property_power": 2700,
                                  "saturation": 0.75, "oil": 3.2, "theory_hOil": 35, "hOil": 48, "revise": 0.65},
                                 {"brake": 2, "speed": 1400, "torque_out": 1300, "torque": 1500, "torque_max": 1600,
                                  "hydraulic_power": 2800, "engine_power": 2400, "engine_full_power": 3000,
                                  "appendix_power": 700, "engine_property_torque": 1600, "engine_property_power": 3100,
                                  "saturation": 0.80, "oil": 3.5, "theory_hOil": 37, "hOil": 50, "revise": 0.70},
                                 ]
                        }
             }
        self.req(p, 'theory/save')

    def testGetPlans(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"model": "SY375H", "manufacturer": "五十铃"}}
             }

        self.req(p, 'theory/getPlans')

    def testPlanLoad(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"planVersion": "v0.1.2_2022-02-15 13:48:40.382423"}}
             }
        self.req(p, 'theory/planLoad')

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass


# if __name__ == '__main__':
#
#     unittest.main()
