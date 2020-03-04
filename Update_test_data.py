#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/4 12:27
# @Author  : 亦轩
# @File    : Update_test_data.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import requests
import pymysql
from DBUtils.PooledDB import PooledDB
import time
import json
from multiprocessing import Queue

POOL = PooledDB(
    # 使用链接数据库的模块
    creator=pymysql,
    # 连接池允许的最大连接数，0和None表示不限制连接数
    maxconnections=6,
    # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    mincached=2,
    # 链接池中最多闲置的链接，0和None不限制
    maxcached=5,
    # 链接池中最多共享的链接数量，0和None表示全部共享。
    # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
    # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
    maxshared=3,
    # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    blocking=True,
    # 一个链接最多被重复使用的次数，None表示无限制
    maxusage=None,
    # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    setsession=[],
    # ping MySQL服务端，检查是否服务可用。
    #  如：0 = None = never, 1 = default = whenever it is requested,
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    ping=0,
    # 主机地址
    host='localhost',
    # 端口
    port=3306,
    # 数据库用户名
    user="root",
    # 数据库密码
    password="root",
    # 数据库名
    database="paper",
    # 字符编码
    charset='utf8'
)
# db_pool = PersistentDB(pymysql, **config)
# # 从数据库连接池是取出一个数据库连接
# SQLconn = db_pool.connection()
# SQLcursor = SQLconn.cursor()
# 创建连接,POOL数据库连接池中
SQLconn = POOL.connection()
# 创建游标
SQLcursor = SQLconn.cursor()

TimeoutSearchResultQuery = Queue()  # 查询状态为 1 时间超时的数据
DayOutSearchResultQuery = Queue()  # 查询 超过15天的数据
SearchResultQuery = Queue()  # 查询状态为检测中的结果数据

def selectDetection():
    current_time = round(time.time() * 1000) - 3600000
    # 查询检测时间 超过1小时 并且状态为1 的数据
    sql = 'select id from detectionlist where iscode=1 and `date`<%d'%current_time
    SQLcursor.execute(sql)
    result = SQLcursor.fetchall()
    for info in result:
        TimeoutSearchResultQuery.put(info)
    # 查询 状态为1 的数据
    sql = 'select id,account_id,taskid from detectionlist where iscode=1 and `date`>%d'%current_time
    SQLcursor.execute(sql)
    result = SQLcursor.fetchall()
    for info in result:
        SearchResultQuery.put(info)
    # 查询检测时间 超过15天 的数据 并清除
    currentday = current_time*24*15
    sql = 'select id from detectionlist where iscode=1 and `date`>%d' % currentday
    SQLcursor.execute(sql)
    result = SQLcursor.fetchall()
    for info in result:
        DayOutSearchResultQuery.put(info)
    print('查询完成')


def timeoutSearchResult():
    while True:
        if not TimeoutSearchResultQuery.empty():
            info = TimeoutSearchResultQuery.get()
            sql = 'update detectionlist set iscode=-2 where id=%d'%info[0]
            SQLcursor.execute(sql)
        else:
            SQLconn.commit()
            break
            time.sleep(60)
        time.sleep(1)
    print('时间超时修改完成')

def searchResult():
    while True:
        if not SearchResultQuery.empty():
            info = SearchResultQuery.get()
            url = 'http://check.vipgz6.idcfengye.com/query/'
            data ={
                'appid':info[1],
                'taskid':info[2]
            }
            res = requests.post(url=url,data=data).text
            data = json.loads(res)['table']
            if data['state'] =='2':
                sql = 'update detectionlist set iscode=2 where id=%d'%info[0]
                SQLcursor.execute(sql)
                SQLconn.commit()
        else:
            break
            time.sleep(60)
        time.sleep(1)
    print('查询中的数据检测完成')

def dayOutSearchResultQuery():
    idstr =''
    while True:
        if not DayOutSearchResultQuery.empty():
            info = DayOutSearchResultQuery.get()
            idstr +=str(info[0]) + ','
        else:
            if idstr:
                idstr = idstr.replace(',','')
                url = '127.0.0.1:8001/delete/data?name=admin&pwd=zz141242&id={}'.format(idstr)
                requests.post(url=url,data=data)
                idstr =''
            break
            time.sleep(60)
        time.sleep(1)
    print('清除超过15天的数据完成')


if __name__ == '__main__':
    selectDetection()
    timeoutSearchResult()
    searchResult()
    print('检测完成')