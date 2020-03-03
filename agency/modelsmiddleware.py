#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/2/29 23:22
# @Author  : 亦轩
# @File    : modelsmiddleware.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import time
from .models import *
import json
import docx


# 判断账户密码是否存在
def account_result(account, pwd):
    '''
    判断账户密码是否存在
    :param account:
    :param pwd:
    :return:
    '''
    try:
        obj = Users.objects.get(account=account, password=pwd)
    except:
        obj = False
    return obj
# 查询账户的剩余次数
def accobj_surplus(accobj):
    '''
    查询账户的剩余次数
    :param accobj:
    :return:
    '''
    try:
        obj = Surplus.objects.get(account=accobj)
        return obj.dic()
    except:
        pass
# 修改账户剩余次数
def surplus_minus(accobj, surp):
    '''
    修改账户剩余次数
    :param account:
    :param surp:
    :return:
    '''
    accountSurplus_obj = Surplus.objects.get(account=accobj)
    if "A" in surp:
        if accountSurplus_obj.a <= 0:
            return False
        accountSurplus_obj.a = accountSurplus_obj.a - 1
    elif 'P' in surp:
        if accountSurplus_obj.p <= 0:
            return False
        accountSurplus_obj.p = accountSurplus_obj.p - 1
    elif 'V' in surp:
        if accountSurplus_obj.v <= 0:
            return False
        accountSurplus_obj.v = accountSurplus_obj.v - 1
    accountSurplus_obj.save()
    return True
# 检测卡查询 并置零
def orderisactivate(order):
    '''
    检测卡查询 并置零
    :param order:
    :return:
    '''
    try:
        obj = isActivateCode.objects.get(isActivate=1, card=order)
        obj.isActivate = False
        obj.save()
        obj = True
    except:
        obj = False
    return obj
# 处理docx文档
def docxfile(path):
    file = docx.Document(path)
    text = ''
    for para in file.paragraphs:
        text += para.text + '\n'
    return text
# 判断文章字数是否符合检测卡
def textLenOrder(numbtext, order):
    '''
    判断文章字数是否符合检测卡
    :param numbtext:
    :param order:
    :return: True/False
    '''
    flag = False
    if order[0] == 'A':
        if numbtext <= 50000:
            flag = True
    elif order[0] == 'P':
        if numbtext <= 150000:
            flag = True
    elif order[0] == 'V':
        if numbtext <= 250000:
            flag = True
    return flag
# 增加检测列表
def addDetection(accobj,order,title,author,iscode,similarity):
    '''
    增加检测列表
    :param accobj:
    :param order:
    :param title:
    :param author:
    :param iscode:
    :param similarity:
    :return:
    '''
    try:
        obj = DetectionList()
        obj.account = accobj
        obj.orderacc = order
        obj.title = title
        obj.author = author
        obj.date = round(time.time() * 1000)
        obj.iscode = iscode
        obj.similarity = similarity
        obj.save()
        return True
    except:
        return False
# 增加错误列表
def addErrot(accobj,order,title,author):
    '''
    增加错误列表
    :param accobj:
    :param order:
    :param title:
    :param auchor:
    :return:
    '''
    try:
        obj = ErrotList()
        obj.account = accobj
        obj.orderacc = order
        obj.title = title
        obj.author = author
        obj.date = round(time.time() * 1000)
        obj.save()
        return True
    except:
        return False