# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.4

@author liuhx

"""
import unittest
import sys
import numpy as np
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

    def testLib(self):
        from instance.utils import simulateRgb

        def points(num):
            # x = np.random.choice(range(100, 200), 1000)
            # y = np.random.choice(range(30, 120), 1000)
            x = np.random.randint(700, 2000, num)
            y = np.random.randint(300, 1200, num)
            # out = np.zeros_like(x)
            z = np.array(list(zip(x, y)))
            # mappings
            m = [{'speed': i[0], 'torque': i[1]} for i in z]
            return m

        num, r = (10325, 50)
        p = points(num)
        print('p', len(p))
        positions = simulateRgb(p, r)
        print('positions', len(positions))
        # self.assertIsNone(positions)
        self.assertEqual(len(positions), len(p))

    def tearDown(self) -> None:
        """
        If the setUp() method raises an exception while the test is running, and the test method will not be executed.
        Similarly, we can provide a tearDown() method that tidies up after the test method has been run:
        """
        pass
