# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

"""
import unittest
import base64
import requests
import json
import pandas as pd
from instance.utils import aes_ecb_encrypt, aes_ecb_decrypted


class TestCommand(unittest.TestCase):

    host = 'localhost'
    port = 6000

    def setUp(self) -> None:
        """
            method called setUp(), which the testing framework will automatically call for every single test we run:
        """
        pass

    # def req(self, p, endPoint, files=None):
    #     pJson = json.dumps(p, ensure_ascii=False).encode('utf-8')
    #     url = "http://{}:{}/".format(self.host, self.port) + endPoint
    #     if files:
    #         response = requests.post(url, {'data': pJson}, files=files) if isinstance(files, dict) else \
    #             requests.post(url, {'data': pJson, 'file': files})
    #     else:
    #         response = requests.post(url, data=pJson, headers={'Content-type': 'application/json'})
    #     print('response', response.text)
    #     response = json.loads(response.text)
    #     self.assertEqual(response['status'], 0)
    #
    # # service
    # def testGetNames(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"model": "SY375H", "manufacturer": "五十铃"}}
    #          }
    #     self.req(p, 'getNames')
    #
    # def testPicLoad(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"picName": "五十铃_485"}}
    #          }
    #     self.req(p, 'picLoad')
    #
    # def testReceive(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"canCode": 1}}
    #          }
    #     file = '../static/量产11档.csv'
    #     self.req(p, 'receive', files={'file': ('量产11档.csv',
    #                                            open(file, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})})
    #
    # def testInputEngine(self):
    #     p = {"model": "SY375H", "manufacturer": "五十铃"}
    #     self.req(p, 'inputEngine')
    #
    # # theory
    # def testCalculate(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"picName": "五十铃_SY375H"},
    #                     "data": [{"brake": 1, "speed": 1000, "torque_out": 1400, "appendix_power": 100, "hOil": 32},
    #                              {"brake": 2, "speed": 1200, "torque_out": 1500, "appendix_power": 105, "hOil": 33},
    #                              {"brake": 3, "speed": 1300, "torque_out": 1600, "appendix_power": 107, "hOil": 34},
    #                              {"brake": 4, "speed": 1400, "torque_out": 1700, "appendix_power": 115, "hOil": 35},
    #                              {"brake": 5, "speed": 1500, "torque_out": 1800, "appendix_power": 117, "hOil": 36},
    #                              {"brake": 6, "speed": 1600, "torque_out": 1900, "appendix_power": 118, "hOil": 37},
    #                              {"brake": 7, "speed": 1700, "torque_out": 2000, "appendix_power": 120, "hOil": 38},
    #                              {"brake": 8, "speed": 1800, "torque_out": 2100, "appendix_power": 130, "hOil": 39},
    #                              {"brake": 9, "speed": 1900, "torque_out": 2200, "appendix_power": 140, "hOil": 41}
    #                              ]
    #                     }
    #          }
    #     self.req(p, 'theory/calculate')
    #
    # def testSave(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"model": "SY375H", "manufacturer": "五十铃", "picName": "test",
    #                              "planName": "1", "planVersion": "v0.1.2"},
    #                     "data": [{"brake": 1, "speed": 1300, "torque_out": 1100, "torque": 1200, "torque_max": 1300,
    #                               "hydraulic_power": 2500, "engine_power": 2100, "engine_full_power": 2600,
    #                               "appendix_power": 500, "engine_property_torque": 1400, "engine_property_power": 2700,
    #                               "saturation": 0.75, "oil": 3.2, "theory_hOil": 35, "hOil": 48, "revise": 0.65},
    #                              {"brake": 2, "speed": 1400, "torque_out": 1300, "torque": 1500, "torque_max": 1600,
    #                               "hydraulic_power": 2800, "engine_power": 2400, "engine_full_power": 3000,
    #                               "appendix_power": 700, "engine_property_torque": 1600, "engine_property_power": 3100,
    #                               "saturation": 0.80, "oil": 3.5, "theory_hOil": 37, "hOil": 50, "revise": 0.70},
    #                              ]
    #                     }
    #          }
    #     self.req(p, 'theory/save')
    #
    # def testGetPlans(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"model": "SY375H", "manufacturer": "五十铃"}}
    #          }
    #
    #     self.req(p, 'theory/getPlans')
    #
    # def testPlanLoad(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"planVersion": "v0.1.2_2022-02-15 13:48:40.382423"}}
    #          }
    #     self.req(p, 'theory/planLoad')
    #
    # # analyze
    # def testAnalyzeCalculate(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"model1": {"picName": "五十铃_SY375H"},
    #                              "model2": {"picName": "五十铃_485"}},
    #                     "data": [{"brake": 1, "speed": 1000, "torque": 1500},
    #                              {"brake": 2, "speed": 1100, "torque": 1600},
    #                              {"brake": 3, "speed": 1200, "torque": 1700},
    #                              {"brake": 4, "speed": 1300, "torque": 1800}
    #                              ]
    #                     }
    #          }
    #     self.req(p, 'analyze/calculate')
    #
    # # compare
    # def testCompareCalculate(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"picName": "五十铃_SY375H"},
    #                     "data": [{"time": "2021-11-30 19:55:12.490", "speed": 1000, "torque(%)": 0.65},
    #                              {"time": "2021-11-30 19:56:12.515", "speed": 1100, "torque(%)": 0.69},
    #                              {"time": "2021-11-30 19:57:12.523", "speed": 1200, "torque(%)": 0.72},
    #                              {"time": "2021-11-30 19:58:12.530", "speed": 1300, "torque(%)": 0.79}
    #                              ]
    #                     }
    #          }
    #     self.req(p, 'compare/calculate')
    #
    # def testCompareSave(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"model": "SY375H",
    #                              "manufacturer": "五十铃",
    #                              "matchPlan": "第二次测试"},
    #                     "data": [{"time": "2021-11-30 19:56:12.490", "speed": 1000, "torque(%)": 0.65,
    #                               "cumOil": 6, "oilFlow": 0.5},
    #                              {"time": "2021-11-30 19:57:12.510", "speed": 2000, "torque(%)": 0.72,
    #                               "cumOil": 7, "oilFlow": 0.6},
    #                              {"time": "2021-11-30 19:58:12.530", "speed": 3000, "torque(%)": 0.85,
    #                               "cumOil": 8, "oilFlow": 0.7}]
    #                     }
    #          }
    #     self.req(p, 'compare/save')
    #
    # def testCompareGetPlans(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"model": "SY375H", "manufacturer": "五十铃"}
    #                     }
    #          }
    #     self.req(p, 'compare/getPlans')
    #
    # def testComparePlanLoad(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"matchPlan": "第二次测试_2022-02-15 14:38:20.274902"}
    #                     }
    #          }
    #     self.req(p, 'compare/planLoad')
    #
    # # contour
    # def testContourConstruct(self):
    #     # 加载负荷数据
    #     data = pd.read_excel('./static/375-6H-国三部分负荷.xlsx', engine='openpyxl')
    #     print('data', data.head())
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"data": list(data.T.to_dict().values())}
    #          }
    #     self.req(p, 'contour/generate')
    #
    # def testContourSave(self):
    #     # 加载负荷数据
    #     data = pd.read_excel('./static/375-6H-国三部分负荷.xlsx', engine='openpyxl')
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"model": "SY375H",
    #                              "manufacturer": "五十铃",
    #                              "picName": "test"},
    #                     "thres": {"rpm_min": 0,
    #                               "rpm_max": 2000,
    #                               "trq_min": 0,
    #                               "trq_max": 2000},
    #                     "data": list(data.T.to_dict().values())
    #                     }
    #          }
    #     # png
    #     png = './instance/tmp/png/tmp_contour_test.png'
    #     with open(png, 'rb') as f:
    #         base64_data = base64.b64encode(f.read())
    #         base64_data = str(base64_data, encoding='utf-8')
    #     self.req(p, 'contour/save', files=base64_data)
    #
    # # history
    # def testHistoryAnalysisUpload(self):
    #     # upload source file
    #     fileObj = open('../static/ShuaiFang_V123_01.csv', 'rb')
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {}
    #          }
    #     self.req(p, 'apis/historyAnalysis/upload', files={'file': ('ShuaiFang_V123_01.csv', fileObj,
    #                                                                'application/vnd.ms-excel', {'Expires': '0'})})
    #
    # def testHistoryAnalysisConf(self):
    #     # upload conf file
    #     fileObj = open('../static/协议配置-V9_0817.txt', 'rb')
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"source": "ShuaiFang_V123_01.csv"}}
    #          }
    #     self.req(p, 'apis/historyAnalysis/conf', files={'file': ('协议配置-V9_0817.txt', fileObj,
    #                                                              'application/vnd.ms-excel', {'Expires': '0'})})
    #
    # def testHistoryAnalysisFigure(self):
    #     p = {"token": "test", "time": 16345323525, "sign": "test",
    #          "params": {"info": {"figure": "1", "conf": "协议配置-V9_0817.txt", "source": "ShuaiFang_V123_01.csv"}
    #                     }
    #          }
    #     self.req(p, 'apis/historyAnalysis/figure')

    # cas
    # def testCAS(self):
    #
    #     p = {"user": "liuhx25", "password": "test"}
    #     self.req(p, 'user-service/login')

    # aes
    def testAES(self):
        p = 'liuhengxin@123测试'
        encrpted = aes_ecb_encrypt(p)
        decrpted = aes_ecb_decrypted(encrpted)
        self.assertEqual(decrpted, p)

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass


# if __name__ == '__main__':
#
#     unittest.main()
