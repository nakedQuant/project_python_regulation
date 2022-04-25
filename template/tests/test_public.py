# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

"""
import unittest
from utils import post_req, get_req


class TestCommand(unittest.TestCase):

    def setUp(self) -> None:
        """
            method called setUp(), which the testing framework will automatically call for every single test we run:
        """
        pass

    def req(self, p, endPoint, files=None):
        self.assertEqual(post_req(p, endPoint, files), 0)

    def testPublicIndex(self):
        self.assertEqual(get_req('index'), 'hello, public')

    # # 需要启动CAS集中认证
    # def testPublicLogin(self):
    #     self.assertEqual(post_req('login'))

    def testPublicUpload(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"picName": "framework"}}
        self.req(p, 'picLoad')

    def testPublicDownload(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {}
             }
        file = '/datasets/test.csv'
        self.req(p, 'receive', files={'file': ('test.csv',
                                               open(file, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})})

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass


# if __name__ == '__main__':
#
#     unittest.main()
