# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def aes_encrypt(raw, style='pkcs7'):
    """
    :param raw: string
    :return:
    """
    # str to bytes
    raw = raw if isinstance(raw, bytes) else raw.encode('utf-8')
    # AES.block_size == 16
    encrypted = cipher.encrypt(pad(raw, AES.block_size, style=style))
    print('encrypted', encrypted)
    utf8_encypted = base64.b64encode(encrypted).decode('utf-8')
    return utf8_encypted


def aes_decrypted(encryption):
    try:
        b64 = json.loads(encryption)
        decryption = {}
        for key, value in b64:
            value = base64.b64decode(value)
            decryption[key] = unpad(cipher.decrypt(value), AES.block_size)
    except json.JSONDecodeError:
        encryption = base64.b64decode(encryption)
        print('decrypted', encryption)
        decryption = unpad(cipher.decrypt(encryption), AES.block_size)
    return decryption.decode('utf-8')


if __name__ == '__main__':

    # init key 长度为 16 倍数
    key = b'bigdataRisk12345'
    cipher = AES.new(key, AES.MODE_ECB)

    result = aes_encrypt('liuhengxin@12344')
    print('result', result)
    assert result == 'H88Rr/E7YsKJMwKiUPyHHN1PzoCj32XikPjTfCDZ/Zo='
    output = aes_decrypted('H88Rr/E7YsKJMwKiUPyHHN1PzoCj32XikPjTfCDZ/Zo=')
    print('output', output)
    result_1 = aes_encrypt('刘恒昕@1234sany')
    print('result', result_1)
    output_1 = aes_decrypted('JOFWljigiK2UuTxMhTeZJ9qnAbgnY7SiF8DIlmTsG0s=')
    print('output 中文', output_1)
