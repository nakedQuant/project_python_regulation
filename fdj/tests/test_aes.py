# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

"""
import unittest
import sys
from pathlib import Path


# 将instance目录纳入
sys.path.append(str(Path(__file__).resolve().parent.parent))


class TestCommand(unittest.TestCase):

    def setUp(self) -> None:
        """
            method called setUp(), which the testing framework will automatically call for every single test we run:
        """
        pass

    # aes
    def testAES(self):
        from instance.utils import aes_ecb_encrypt, aes_ecb_decrypted
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
