#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/4 12:27
# @Author  : 亦轩
# @File    : Update_test_data.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import requests
import pymysql
import time
import json
from multiprocessing import Queue

# user = 'root'
# password = 'root'
# database = 'paper'
user = 'www_cnkidata_com'
password = 'yzdeY64CDDXYBf6w'
database = 'www_cnkidata_com'
loaclurl = '47.244.144.152'
class Crawler(object):
    def __init__(self):
        self.url = 'http://api.cnkin.net/'
        # 连接database
        self.localurl = 'http://www.cnkidata.com/'
        self.conn = pymysql.connect(host=loaclurl, user =user, password =password, database =database, charset ='utf8')
        # 得到一个可以执行SQL语句的光标对象
        self.cursor = self.conn.cursor()
        self.TimeoutSearchResultQuery = Queue()  # 查询状态为 1 时间超时的数据
        self.DayOutSearchResultQuery = Queue()  # 查询 超过15天的数据
        self.SearchResultQuery = Queue()  # 查询状态为检测中的结果数据

    def selectDetection(self):
        current_time = round(time.time() * 1000) - 1800000
        # 查询检测时间 超过1小时 并且状态为1 的数据
        sql = 'select id from detectionlist where iscode=1 and `date`<%d'%current_time
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print('状态为1的数据',len(result))
        for info in result:
            self.TimeoutSearchResultQuery.put(info)
        # 查询 状态为1 的数据
        sql = 'select id,account_id,taskid from detectionlist where iscode=1 and `date`>%d'%current_time
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for info in result:
            self.SearchResultQuery.put(info)
        # 查询检测时间 超过15天 的数据 并清除
        currentday = current_time*24*15
        sql = 'select id from detectionlist where iscode=1 and `date`>%d' % currentday
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for info in result:
            self.DayOutSearchResultQuery.put(info)
        print('查询完成')

    def timeoutSearchResult(self):
        while True:
            if not self.TimeoutSearchResultQuery.empty():
                info = self.TimeoutSearchResultQuery.get()
                sql = 'update detectionlist set iscode=-2 where id=%d'%info[0]
                self.cursor.execute(sql)
                self.conn.commit()
            else:
                break
                time.sleep(60)
            time.sleep(1)
        print('时间超时修改完成')

    def searchResult(self):
        '''
        查询状态为1的数据是否完成
        完成后打包
        :return:
        '''
        while True:
            if not self.SearchResultQuery.empty():
                info = self.SearchResultQuery.get()
                data ={
                    'appid':info[1],
                    'taskid':info[2]
                }
                res = requests.post(url=self.url+'/query/',data=data).text
                if isinstance(res,str):
                    res = json.loads(res)
                if res['result'] =='0':
                    continue
                data = res['table']
                if data['state'] =='2':
                    sql = 'update detectionlist set iscode=4,similarity={} where id={}'.format(res['checkResult']['similarity'],info[0])
                    self.cursor.execute(sql)
                    self.conn.commit()
                    pathurl = self.localurl + '/agency/file/package?name=admin&pwd=zz141242&id={}'.format(info[0])
                    requests.get(url=pathurl)
            else:
                break
                time.sleep(60)
            time.sleep(1)
        print('查询中的数据检测完成')

    def dayOutSearchResultQuery(self):
        '''超过15天的数据, 删除'''
        idstr =''
        while True:
            if not self.DayOutSearchResultQuery.empty():
                info = self.DayOutSearchResultQuery.get()
                idstr +=str(info[0]) + ','
            else:
                if idstr:
                    idstr = idstr.replace(',','')
                    pathurl = self.localurl + '/agency/delete/data?name=admin&pwd=zz141242&id={}'.format(idstr)
                    requests.post(url=pathurl)
                break
            time.sleep(1)
        print('清除超过15天的数据完成')

    def deletes(self):
        # 关闭光标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()
        print('关闭系统资源')
        # self.close()

if __name__ == '__main__':
    while True:
        try:
            crawler = Crawler()
            crawler.selectDetection()
            crawler.timeoutSearchResult()
            crawler.searchResult()
            crawler.deletes()
            print('检测完成')
        except:
            print('\t\t\t\t\t\t查询发生错误')
        time.sleep(10)