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
import requests
# 发送论文检测
def post_jiance(name,author,title,fulltext):
    '''
    检测论文
    :param name:
    :param author:
    :param title:
    :param fulltext:
    :return:
    '''
    url = 'http://check.vipgz6.idcfengye.com/post/'
    data = {
        'appid': name,
        'author': author,
        'title': title,
        'content': fulltext,
    }
    try:
        res = requests.post(url, data=data).text
        resdata = json.loads(res)
        if resdata['result'] == '1':
            taskid = resdata['returnval']
            iscode = 1
            return taskid,iscode
    except:
        pass
    # 送论文检测错误
    return '',-2
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
        obj = IsActivateCode.objects.get(isActivate=0, card=order)
        obj.isActivate = True
        obj.save()
        obj = True
    except:
        obj = False
    return obj
# 处理docx文档
def docxfile(path):
    '''
    处理docx文档 返回文章字符串
    :param path:
    :return:
    '''
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
def addDetection(accobj,order,title,author,taskid,iscode,path):
    '''
    增加检测列表
    :param accobj:
    :param order: 订单编号
    :param title:
    :param author:
    :param taskid:
    :return:
    '''
    try:
        obj = DetectionList()
        obj.account = accobj
        obj.orderacc = order
        obj.title = title
        obj.author = author
        obj.date = round(time.time() * 1000)
        obj.taskid = taskid
        obj.filepath = path
        obj.iscode = iscode
        obj.save()
        return True
    except:
        return False
# 查询检测列表
def selectDetection(accobj,page=0,rows=0,title=''):
    '''
    查询 检测列表
    :param accobj: 用户 obj
    :param page:  页数
    :param number: 每页多个个
    :return: 列表
    '''
    if page and rows:
        start = int(rows) * (int(page) -1)
        end = int(page) * int(rows)+1
    else:
        start=None
        end=None
    if title:
        obj_list=DetectionList.objects.filter(account=accobj,title__contains=title).order_by('-id')[start:end]
    else:
        obj_list = DetectionList.objects.filter(account=accobj).order_by('-id')[start:end]
    obj_list_dict =[]
    for obj in obj_list:
        obj_list_dict.append(obj.dic())
    return obj_list_dict
# 重新检测检测失败并扣分的文章
def resubmit(accobj,ids):
    # try:
        obj = DetectionList.objects.get(id=ids,iscode=-2,account=accobj)
        name = accobj.account
        author = obj.author
        title = obj.title
        filepath = obj.filepath
        if 'docx' in filepath.split('.'[-1]):
            fulltext = docxfile(filepath)
        else:
            with open(filepath,'r') as f:
                fulltext = f.read()
        taskid,iscode = post_jiance(name,author,title,fulltext)
        obj.taskid = taskid
        obj.iscode = iscode
        obj.data = round(time.time() * 1000)
        obj.save()
    # except:
    #     pass
# 查询文件路径
def selectfilepath(id):
    filepath = DetectionList.objects.values('id','filepath').filter(id=id)[0]
    return filepath['filepath']

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


def deletedata15day(id):
    try:
        obj = DetectionList.objects.get(id=id)
        obj.delete()
    except:
        pass