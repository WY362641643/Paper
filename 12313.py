#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/12 1:58
# @Author  : 亦轩
# @File    : 12313.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import re
ss = ' /cnki/report/tid/2222222222222/sid/12'
s = re.findall('/report/tid/(?P<order>\s{12,32}|\d{12,32})/sid/(?P<id>\d+)',ss)
print(s)