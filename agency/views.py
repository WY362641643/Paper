from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
import json
import time
import os
from . import modelsmiddleware as MDW
from django.conf import settings
import requests


# Create your views here.

def index_views(request):
    # print("/")
    if request.method == 'GET':
        if 'sname' in request.session:
            name = request.session['sname']
            pwd = request.session['spwd']
            users = MDW.account_result(name, pwd)
            if users:
                message = MDW.accobj_surplus(users)
                message['account'] = name
                return render(request, 'main.html', locals())  # 从哪来,回哪去
            else:
                del request.session['sname']
                del request.session['spwd']
                return render(request, 'login.html')  # 返回登录页面
        else:
            if 'cname' in request.COOKIES and 'cpwd' in request.COOKIES:
                try:
                    name = request.COOKIES['cname']
                    name = json.loads(name)
                    pwd = request.COOKIES['cpwd']
                except:
                    resp = render(request, 'login.html')
                    resp.delete_cookie('cname')
                    resp.delete_cookie('cwd')
                    return resp  # 返回登录页面
                users = MDW.account_result(name, pwd)
                if users:
                    # 添加 session
                    request.session['sname'] = name
                    request.session['spwd'] = pwd
                    message = MDW.accobj_surplus(users)
                    message['account'] = name
                    return render(request, 'main.html', locals())
                else:
                    resp = render(request, 'login.html')
                    resp.delete_cookie('cname')
                    resp.delete_cookie('cwd')
                    return resp  # 返回登录页面
            else:
                return render(request, 'login.html')  # 返回登录页面
    else:
        username = request.POST['username']  # 接收用户名
        password = request.POST['password']  # 接收密码
        user_obj = MDW.account_result(username, password)
        if user_obj:
            if 'remember' in request.POST:
                request.session['sname'] = username
                request.session['spwd'] = password
                resp = redirect("/login")
                resp.set_cookie('cname', username, 60 * 60 * 24 * 365 * 5)
                resp.set_cookie('cpwd', password, 60 * 60 * 24 * 365 * 5)
                return resp
            else:
                # 正确
                # print('记住密码1小时 账号正确')
                # username = str(username).encode('utf-8')
                # print(username)
                # print('用户名称%s,用户密码%s' % (username, password))
                request.session['sname'] = username
                request.session['spwd'] = password
                resp = redirect("/login")
                # print('用户名称%s == 用户密码%s' % (username, password))
                # 添加cookie
                # username = username.decode('utf-8')
                un2 = json.dumps(username)
                resp.set_cookie('cname', username, 60)
                resp.set_cookie('cpwd', password, 60)
                # print(resp)
                # print("接收到账号密码登录")
                return resp
        else:
            return render(request, 'login.html')  # 返回登录页面


# 手工检测
def detection(request):
    if 'sname' in request.session:
        accobj = MDW.account_result(request.session['sname'],request.session['spwd'])
        if not accobj:
            return render(request,'login.html')
        if request.method == 'GET':
            return render(request, 'detection.html', locals())
        else:
            types = request.POST['select']
            title = request.POST['title']
            fulltext = request.POST['fulltext']
            if not MDW.textLenOrder(len(fulltext),types):
                jsonStr = {
                    'result': 0,
                    'message': 'NUMBER_OF_WOEDS_NOT'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            if 'author' in request.POST:
                author = request.POST['author']
            else:
                author = ''
            if not MDW.surplus_minus(accobj, types):
                jsonStr = {
                    'result': 0,
                    'message': 'AGENT_BALANCE_NOT_ENOUGH'
                }
            else:
                url = 'http://2935q843e4.goho.co:48269/post'
                data = {
                    'appid': request.session['sname'],
                    'author': author,
                    'title': title,
                    'content': fulltext,
                }
                res = requests.post(url, data=data).text
                print(res)
                jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')


# 批量检测
def upload(request):
    if 'sname' in request.session:
        accobj = MDW.account_result(request.session['sname'], request.session['spwd'])
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'upload.html', locals())
        else:
            # 获取前端传输的文件对象
            file_obj = request.FILES.get('file')
            # 获取文件类型
            file_type = file_obj.name.split('.')[-1]
            # 将文件类型中的数据大写全部转换成小写
            file_type = file_type.lower()
            # 将文件存到指定目录
            # 获取当前时间的时间戳
            timestr = str(time.time()).replace('.', '')
            # 获取程序需要写入的文件路径
            path = os.path.join(settings.BASE_DIR, 'static/file/{0}{1}'.format(timestr, file_obj.name))
            # 根据路径打开指定的文件(以二进制读写方式打开)
            f = open(path, 'wb+')
            # chunks将对应的文件数据转换成若干片段, 分段写入, 可以有效提
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            order, author, title, select, types = file_obj.name.split('_')
            text = MDW.docxfile(path)
            if not MDW.textLenOrder(len(text), order):
                jsonStr = {
                    'result': 0,
                    'message': 'AGENT_BALANCE_NOT_ENOUGH'
                }
            if not MDW.surplus_minus(accobj, types):
                jsonStr = {
                    'result': 0,
                    'message': 'AGENT_BALANCE_NOT_ENOUGH'
                }
            else:
                if False:
                    url = 'http://182.92.117.192:8811/swagger-ui.html#!/apply-web/postCheckUsingPOST'
                    data = {
                        'appid': request.session['sname'],
                        'author': author,
                        'title': title,
                        'content': fulltext
                    }
                    res = requests.post(url, data=data).text
                    print(res)
                jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')


# 检测列表
def detectionlist(request):
    if 'sname' in request.session:
        if request.method == 'GET':
            message = {
                'id': 0,  # 文件ID
                'taskid': '',  # 操作需要的随机编号
                'orderid': 1234651324651564, # 订单编号
                'title': '测试标题',
                'author': '测试作者',
                'state': -2,    # 状态  -2:文件解析出错, -1:待提交 0:待检测,1:正在检测,2;等待获取报告,3正在生成报告,4:检测完成,其他:未知
                'postTime': '123465465156456',  # 表示自UTC 1970年1月1日午夜之后经过的毫秒数
                'similarity': 50,  # 相似度
            }
            return render(request, 'list.html', locals())
        else:
            message = {'serverAndDomain_fmt': {'value': '', 'row': {'serverName': 'www', 'domain': 'zzz'}, 'index': ''},
                       'fmt_matchNo': {'value': 0, 'row': '', 'rowIndex': ''},
                       }
            return HttpResponse(json.dumps(message), content_type="application/json")
    return render(request, 'login.html')


# 错误列表
def errorlist(request):
    if 'sname' in request.session:
        if request.method == 'GET':
            return render(request, 'error.html', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')


# 打包文档
def docpack(request):
    if 'sname' in request.session:
        if request.method == 'GET':
            return render(request, 'doc.html', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')


# 订单管理
def order(request):
    if 'sname' in request.session:
        if request.method == 'GET':
            return render(request, 'order.html', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')


# 宝贝管理
def product(request):
    if 'sname' in request.session:
        if request.method == 'GET':
            return render(request, 'product.html', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')


# 个人资料
def user_info(request):
    if 'sname' in request.session:
        if request.method == 'GET':
            return render(request, 'user_info.htm', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')


# 修改密码
def user_chpwd(request):
    if 'sname' in request.session:
        if request.method == 'GET':
            return render(request, 'user_chpwd.htm', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')


# 用户退出登录
def logout(request):
    if request.method == "GET":
        try:
            del request.session['sname']
            del request.session['spwd']
            resp = render(request, 'login.html')
            resp.delete_cookie('cname')
            resp.delete_cookie('cwd')
            return resp  # 返回登录页面
        except:
            return render(request, 'login.html')
