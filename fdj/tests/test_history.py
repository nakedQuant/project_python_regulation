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

    # history
    def testHistoryAnalysisUpload(self):
        # upload source file
        fileObj = open('../static/ShuaiFang_V123_01.csv', 'rb')
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {}
             }
        self.req(p, 'apis/historyAnalysis/upload', files={'file': ('ShuaiFang_V123_01.csv', fileObj,
                                                                   'application/vnd.ms-excel', {'Expires': '0'})})

    def testHistoryAnalysisConf(self):
        # upload conf file
        fileObj = open('../static/协议配置-V9_0817.txt', 'rb')
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"source": "ShuaiFang_V123_01.csv"}}
             }
        self.req(p, 'apis/historyAnalysis/conf', files={'file': ('协议配置-V9_0817.txt', fileObj,
                                                                 'application/vnd.ms-excel', {'Expires': '0'})})

    def testHistoryAnalysisFigure(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"figure": "1", "conf": "协议配置-V9_0817.txt", "source": "ShuaiFang_V123_01.csv"}
                        }
             }
        self.req(p, 'apis/historyAnalysis/figure')

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass


# if __name__ == '__main__':
#
#     unittest.main()
