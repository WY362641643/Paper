#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/6 14:46
# @Author  : 亦轩
# @File    : 22.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import requests
import json
import time
from hashlib import md5

s = 'A_111111111111111111_牡蛎君_标色辅助修改.docx'
t = s.split('_')[-2:]
# 加密
def get_md5(link:str):
    if isinstance(link, str):
        link = link.encode('utf-8')
    m = md5()
    m.update(link)
    return m.hexdigest()
m = get_md5(s)
print(m)
print(len(m))