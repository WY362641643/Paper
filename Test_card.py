#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/1 19:05
# @Author  : 亦轩
# @File    : Test_card.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import datetime
import random
from hashlib import md5
from DBUtils.PooledDB import PooledDB
import pymysql
import time
source = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v',
    'b', 'n', 'm',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
]
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
    # # 主机地址
    host='47.244.144.152',
    # # 端口
    # port=13306,
    # 主机地址
    # host='localhost',
    # 端口
    port=3306,
    # 数据库用户名
    user="www_cnkidata_com",
    # 数据库密码
    password="yzdeY64CDDXYBf6w",
    # 数据库名
    database="www_cnkidata_com",
    # 字符编码
    charset='utf8'
)
# 创建连接,POOL数据库连接池中
SQLconn = POOL.connection()
# 创建游标
SQLcursor = SQLconn.cursor()

# 加密
def get_md5(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    m = md5()
    m.update(text)
    return m.hexdigest()


def crea_iscode(numbers,types):
    sql = 'INSERT INTO isactivatecode (card,isactivate) VALUES(%s,0) '
    for _ in range(numbers):
        s = ''.join(random.sample(source, 5))
        card = types + get_md5(types + s + 'zz141242')[0:6] + s
        try:
            SQLcursor.executemany(sql, [(card)])
        except pymysql.err.IntegrityError:
            continue
        SQLconn.commit()
    SQLconn.close()


if __name__ == '__main__':
    # crea_iscode(15,'A',20)
    flag = True
    while True:
        types = input('''
        + =================================+
        |  1)  A 类型 5W字符以内           |
        |  2)  P 类型 10W字符以内          |
        |  3)  V 类型 25W字符以内          |
        |  q)  退出                        |
        +==================================+
        请输入: ''')
        if types == '1':
            types = 'A'
            break
        elif types == '2':
            types = 'P'
            break
        elif types == '3':
            types = 'V'
            break
        elif types == 'q':
            flag = False
            break
        else:
            print('输入错误, 请重新输入: ')
    if flag:
        while True:
            try:
                numbers = int(input('请输入生成的数量:'))
                break
            except:
                print('输入错误, 请重新输入: ')
        try:
            crea_iscode(numbers,types)
            print('生成完成')
        except:
            print('生成错误')
        time.sleep(3)