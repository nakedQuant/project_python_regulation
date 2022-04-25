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

    # service
    def testGetNames(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"model": "SY375H", "manufacturer": "五十铃"}}
             }
        self.req(p, 'getNames')

    def testPicLoad(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"picName": "五十铃_485"}}
             }
        self.req(p, 'picLoad')

    def testReceive(self):
        p = {"token": "test", "time": 16345323525, "sign": "test",
             "params": {"info": {"canCode": 1}}
             }
        file = '../static/量产11档.csv'
        self.req(p, 'receive', files={'file': ('量产11档.csv',
                                               open(file, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})})

    def testInputEngine(self):
        p = {"model": "SY375H", "manufacturer": "五十铃"}
        self.req(p, 'inputEngine')

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass


# if __name__ == '__main__':
#
#     unittest.main()
