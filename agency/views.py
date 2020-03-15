from django.shortcuts import render, redirect
from django.http import HttpResponse,FileResponse
import json
import time
import requests
from hashlib import md5
import os
import random
from . import modelsmiddleware as MDW
from django.conf import settings
import urllib.parse as up
from agency.models import *
from agency.sign import Sign
# Create your views here.
source = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
]
sourcetitle = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C',
          'V', 'B', 'N', 'M',
          'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'j', 'h', 'k', 'l', 'm', 'n', 'b',
          'v', 'c', 'x', 'z',
          '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
          ]
def index_views(request):
    # print("/")
    if request.method == 'GET':
        if 'sname' in request.session:
            name = request.session['sname']
            pwd = request.session['spwd']
            users = MDW.account_result(name, pwd)
            if users:
                message = MDW.accobj_surplus(users)
                if not message:
                    message= {
                        'A': 0,
                        'P': 0,
                        'V': 0,
                    }
                else:
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
                resp = redirect("/agency/login")
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
                resp = redirect("/agency/login")
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
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request,'login.html')
        if request.method == 'GET':
            return render(request, 'detection.html', locals())
        else:
            if 'select' not in request.POST:
                #　未选择系统类型
                jsonStr = {
                    'result': 0,
                    'message': 'NUMBER_OF_WOEDS_NOT'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            types = request.POST['select']
            title = request.POST['title']
            fulltext = request.POST['fulltext']
            # 判断 字符数 是否符合 系统类型
            if not MDW.textLenOrder(len(fulltext),types):
                jsonStr = {
                    'result': 0,
                    'message': 'NUMBER_OF_WOEDS_NOT'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            if 'author' in request.POST:
                author = request.POST['author']
            else:
                author = name
            if not MDW.surplus_minus(accobj, types):
                jsonStr = {
                    'result': 0,
                    'message': 'AGENT_BALANCE_NOT_ENOUGH'
                }
            else:
                timestr = str(time.time()).replace('.', '')
                filename = str(types)+'_'+str(author)+'_'+str(title)+'.txt'
                path = os.path.join(settings.BASE_DIR, 'static/file/{0}{1}'.format(timestr, filename))
                # 根据路径打开指定的文件
                with open(path, 'a',encoding='utf-8') as f:
                    f.write(fulltext)
                taskid,iscode = MDW.post_jiance(name,author,title,fulltext)
                word_number_text = len(fulltext)
                orders = str(types) + str(''.join(random.sample(source, 14)))
                MDW.addDetection(accobj, orders, title, author, taskid, iscode,path,len(fulltext))
                jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 批量检测
def upload(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'upload.html', locals())
        else:
            # 获取前端传输的文件对象
            file_obj = request.FILES.get('file')
            try:
                order, author, title = file_obj.name.split('_')
            except:
                jsonStr = {
                    'result': 0,
                    'message': '未识别文件名或文件名错误'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            if not MDW.select_order_account(order):
                jsonStr = {
                    'result': 0,
                    'message': '订单号错误,或者商家剩余积分不足, 请联系客服'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            # 获取当前时间的时间戳
            timestr = ''.join(random.sample(source, 2))
            # 获取后缀
            suffix = file_obj.name.split(".")[-1]
            # 获取程序需要写入的文件路径
            path = os.path.join(settings.BASE_DIR, 'static/file/{0}{1}'.format(timestr, file_obj.name))
            # 根据路径打开指定的文件(二进制形式打开)
            f = open(path, 'wb+')
            # chunks将对应的文件数据转换成若干片段, 分段写入, 可以有效提
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            try:
                if suffix == 'docx':
                    text = MDW.filedocx(path)
                elif suffix == 'txt':
                    text = MDW.filetxt(path)
                elif suffix == 'doc':
                    text = MDW.filedoc(path)
                # elif suffix == 'wps':
                #     text = MDW.filewps(path)
                else:
                    raise ValueError
            except:
                jsonStr = {
                    'result': 0,
                    'message': '论文文件内容格式错误'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            # 获取文章字符数
            word_number_text = len(text)
            status,types = MDW.textLentaobaoOrder(word_number_text,order)
            if not status:
                jsonStr = {
                    'result': 0,
                    'message': types
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            # 查询账户剩余积分是否够用
            # if not MDW.surplus_shengyu(accobj, pattern):
            #     jsonStr = {
            #         'result': 0,
            #         'message': '该系统剩余积分不足, 请充值'
            #     }
            #     return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            taskid,iscode = MDW.post_jiance(name,author,title,text)
            if not MDW.addDetection(accobj,order, title, author, taskid, iscode,path,word_number_text):
                jsonStr = {
                    'result': 0,
                    'message': '添加检测失败'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            MDW.surplus_order_minus(order)
            MDW.gods_up(order)
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 用户前端检测  # 废弃
def upload_user(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'upload.html', locals())
        else:
            # 获取前端传输的文件对象
            file_obj = request.FILES.get('file')
            try:
                title_package = file_obj.name.split('_')
                if len(title_package) ==3:
                    order, author, title = title_package
                elif len(title_package) ==2:
                    author, title = title_package
                elif len(title_package) ==1:
                    title = title_package
                else:
                    jsonStr = {
                        'result': 0,
                        'message': '未识别文件名'
                    }
                    return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            except:
                jsonStr = {
                    'result': 0,
                    'message': '文件命名规则错误'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            if order and len(order)==1:
                if not MDW.surplus_minus(accobj, order):
                    jsonStr = {
                        'result': 0,
                        'message': '此系统类型剩余次数不足'
                    }
                    return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            elif len(str(order)) == 18:
                print('这里请求淘宝')
            elif not MDW.orderisactivate(order):
                jsonStr = {
                    'result': 0,
                    'message': '检测卡错误或已激活'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            # 获取当前时间的时间戳
            timestr = str(time.time()).replace('.', '')
            # 获取后缀
            suffix = file_obj.name.split['.'][-1]
            # 获取程序需要写入的文件路径
            path = os.path.join(settings.BASE_DIR, 'static/file/{0}{1}'.format(timestr, file_obj.name))
            # 根据路径打开指定的文件(二进制形式打开)
            f = open(path, 'wb+')
            # chunks将对应的文件数据转换成若干片段, 分段写入, 可以有效提
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            if suffix == 'docx':
                try:
                    text = MDW.docxfile(path)
                except:
                    jsonStr = {
                        'result': 0,
                        'message': '论文文件内容格式错误'
                    }
                    return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            try:
                int(order)
            except ValueError:
                if not MDW.textLenOrder(len(text), order[0]):
                    jsonStr = {
                        'result': 0,
                        'message': '文章字符数过多,请选择其他激活卡或系统类型'
                    }
                    return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            taskid,iscode = MDW.post_jiance(name,author,title,text)
            MDW.addDetection(accobj,order, title, author, taskid, iscode,path)
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 检测列表
def detectionlist(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            message = MDW.selectDetection(accobj)
            return render(request, 'list.html', locals())
        else:
            page = request.POST['page']
            rows = request.POST['rows']
            if 'title' in request.POST:
                title = request.POST['title']
            else:
                title = ''
            message = MDW.selectDetection(accobj,page,rows,title)
            return HttpResponse(json.dumps(message), content_type="application/json")
    return render(request, 'login.html')
# 重新检测检测失败并扣分的文章
def resubmit(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            ids = request.GET.get('id')
            MDW.resubmit(accobj,ids)
            return HttpResponse('<h1>提交成功</h>')
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 删除超过 15天的数据
def deletedata(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        pwd = request.GET.get('pwd')
        id = request.GET.get('id')
        if name=='admin' and pwd == 'zz141242':
            MDW.deletedata15day(id)
        return True
#下载原文
def textdownload(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        id = request.GET.get('id')
        filepath = MDW.selectfilepath(id)
        if not filepath:
            return HttpResponse('<h1>原文已删除</h1>')
        filename = up.quote("_".join(filepath.split('/')[-1].split('_')[1:]))
        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
        return response
# 批量下载文件
def batchDownload(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        ids = request.GET.get('ids')
        filepathlist =[]
        timestr = str(time.time()).replace('.', '')
        zippath = os.path.join(settings.BASE_DIR, 'static/fileszip/{0}{1}'.format(timestr, '.zip'))
        MDW.zipDir(filepathlist,'static/file/',zippath)
        filename = zippath.split('/')[-1]
        file = open(zippath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
        return response
# 错误列表
def errorlist(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'error.html', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 打包 检测成功的 文档
def file_package(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        pwd = request.GET.get('pwd')
        id = request.GET.get('id')
        jsonStr = {"result": 0, "message": ''}
        if name=='admin' and pwd == 'zz141242':
            if not MDW.post_examiningz_report(id):
                jsonStr = {"result": 1,  "message": '请求接口错误'}
        return HttpResponse(json.dumps(jsonStr), content_type="application/json")
# 下载检测报告
def examining_report(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            id = request.GET.get('id')
            zippath = MDW.post_examiningz_report(id)
            if not zippath:
                return HttpResponse('<h1>下载失败: 请求接口错误</h1>')
            filename = zippath.split('/')[-1]
            filename = up.quote(filename)
            file = open(zippath, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
            return response
        else:
            id = request.GET.get('id')
            zippath = MDW.post_examiningz_report(id, True)
            if zippath:
                jsonStr = {"result": 1, "message": '打包成功'}
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            else:
                jsonStr = {"result": 0, "message": '打包失败,请求接口错误'}
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 查询代理商 上传的 广告文档
def docpack(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            message = MDW.create(accobj)
            return render(request, 'doc.html')
        else:
            message = MDW.create(accobj)
            return HttpResponse(json.dumps(message), content_type="application/json")
    return render(request, 'login.html')
# 增加 代理商 上传的 广告文档
def addDocPack(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'doc.html', locals())
        else:
            file_obj = request.FILES.get('file')
            # 获取当前时间的时间戳
            timestr = str(random.randint(1,99999))
            # 获取程序需要写入的文件路径
            filename = timestr + '_'+ file_obj.name
            path = os.path.join(settings.BASE_DIR, 'static/fileadvert/{}'.format(filename))
            if os.path.exists(path):
                jsonStr = {"result": 0, "massage": '失败,文件名已存在'}
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            # 根据路径打开指定的文件(二进制形式打开)
            f = open(path, 'wb+')
            # chunks将对应的文件数据转换成若干片段, 分段写入, 可以有效提
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            MDW.addpack(filename,accobj)
            jsonStr = {"result": 1, "massage": '上传成功'}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 删除 代理商 上传的广告文档
def deletedoc(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            ids = request.GET.get('ids')
            ids = ids.split(',')
            if MDW.deletdoc(accobj,ids):
                jsonStr = {"result": 1, "message": '删除成功'}
            else:
                jsonStr = {"result": 0, "message": '删除失败, 未查询到信息'}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 订单管理
def order(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'order.html', locals())
        else:
            message = MDW.select_order(accobj)
            return HttpResponse(json.dumps(message), content_type="application/json")
    return render(request, 'login.html')
# 清空订单可用件数
def order_clear(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            orderid = request.GET.get('orderid')
            msg = MDW.clear_order_num(accobj,orderid)
            if msg:
                message={"result": 1,  "message": '清空成功'}
            else:
                message = {"result": 0, "message": '清空失败'}
            return HttpResponse(json.dumps(message), content_type="application/json")
    return render(request, 'login.html')
# 宝贝管理
def product(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'product.html')
        else:
            jsonStr = MDW.select_product(accobj)
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 个人资料
def user_info(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'user_info.htm', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# 修改密码
def user_chpwd(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
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
# 推送订单保存
def order_put(request):
    if request.method == 'POST':
        try:
            aopic = request.GET.get('aopic')
            sign = request.GET.get('sign')
            timestamp = request.GET.get('timestamp')
            json_data = request.POST.get('json')
            f = open('推送json串.txt','a')
            f.write(json_data+'\n')
            f.write(str(aopic) + '\n')
            f.write(str(sign) + '\n')
            f.write(str(timestamp) + '\n')
            # if Sign(timestamp, json_data) != sign:
            #     return HttpResponse('验签失败')
            # 订单推送,插入表订单信息等数据
            if aopic == "21" or aopic == 21 or aopic == "2" or aopic == 2 or aopic == "1" or aopic == 1:
                all_data = json.loads(json_data)
                tid = all_data['Tid']  # 订单号
                # account = all_data['SellerNick']  # 代理商
                treid = all_data['Orders'][0]['NumIid']  # 宝贝id
                # WW = all_data['BuyerNick']  # 旺旺
                payment = all_data['Payment']  # 实付金额
                quantity_residual = all_data['Num']  # 数量
                date = all_data['PayTime']  # 付款日期
                if date == None or date == "null":
                    date = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                f.write(str(tid) + '\n')
                f.close()
                treasure = Treasure.objects.get(treid=treid)
                xitong = treasure.xitong
                account_id = treasure.account
                order = Order()
                order.types = xitong
                order.account = account_id
                order.ordernumber = tid
                order.date = date
                order.quantity_residual = quantity_residual
                order.payment = payment
                order.save()

                return HttpResponse('验签成功,保存数据成功')
            # 退款订单推送，删除订单等信息
            elif aopic == "256" or aopic == 256:
                # {"Tid":888710912223440387,"Oid":888710912223440387,"RefundId":56043394560448703,"SellerNick":"金榜教育服务","BuyerNick":"爱尚乐购8","RefundFee":"35.00","RefundPhase":"onsale","BillType":"refund_bill","Modified":"2020-03-13 16:35:58"}
                all_data = json.loads(json_data)
                tid = all_data['Tid']  # 订单号
                try:
                    o = Order.objects.get(ordernumber=tid)
                    o.freeze = True
                    o.save()
                    # d = DetectionList.objects.get(orderacc=tid)
                    # d.iscode = 5
                    # d.save()
                except:
                    return HttpResponse('买家申请退款失败')
                return HttpResponse('买家申请退款')
            # 撤销退款订单推送，需重新增加订单信息
            elif aopic == "32768" or aopic == 32768:
                try:
                    all_data = json.loads(json_data)
                    tid = all_data['Tid']  # 订单号
                    o = Order.objects.get(ordernumber=tid)
                    o.freeze = False
                    o.save()
                    # d = DetectionList.objects.get(orderacc=tid)
                    # d.iscode = 0
                    # d.save()
                except:
                    return HttpResponse('买家撤销退款失败')
                return HttpResponse('买家撤销退款')
            else:
                return HttpResponse('未知推送')
        except Exception as e:
            return HttpResponse('验签错误:%s'%str(e))
# 无需物流发货
def gods_up(request):
    if request.method == "POST":
        tids = request.POST.get('tids')    #订单号
        url = "http://gw.api.agiso.com/alds/Trade/LogisticsDummySend"   # 请求链接
        timestamp = str(int(time.time()))
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "ApiVersion ": "1",
            "Authorization": "Bearer TbAldsee25p739wafxdz5u88uxxrfxtrydp6eh62htatkuggf5",
        }
        s = ("p8hbc7zvurx6ckyzu5hxteyf6ykhky9w" + "tids"+str(tids) + "timestamp" + timestamp + "p8hbc7zvurx6ckyzu5hxteyf6ykhky9w").encode('utf8')
        ms = md5(s).hexdigest()
        data = {
            "tids":str(tids),
            "timestamp": timestamp,
            "sign": ms
        }
        res = requests.post(url,data=data,headers=headers)
        json_hmtl = res.text
        # {"IsSuccess":true,"Data":null,"Error_Code":0,"Error_Msg":"","AllowRetry":null}
        html = json.loads(json_hmtl)
        if html['Error_Code'] != 0:
            jsonStr = {"result": "验签错误"}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
        if html['Data']:
            jsonStr = {"result": "发货成功"}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
        jsonStr = {"result": html['Data']}
        return HttpResponse(json.dumps(jsonStr), content_type="application/json")
# 获取商家信息
def seller_info(request):
    if request.method == "POST":
        numIid = request.POST.get('treid')    # 获取宝贝id
        url = "http://gw.api.agiso.com/alds/Item/SellerGet"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "ApiVersion ": "1",
            "Authorization": "Bearer TbAldsee25p739wafxdz5u88uxxrfxtrydp6eh62htatkuggf5",
        }
        timestamp = str(int(time.time()))
        fields = "nick"
        s = ("p8hbc7zvurx6ckyzu5hxteyf6ykhky9w" + "fields" + str(fields) + "numIid" + str(numIid) + "timestamp" + timestamp + "p8hbc7zvurx6ckyzu5hxteyf6ykhky9w").encode('utf8')
        ms = md5(s).hexdigest()
        data = {
            "fields": fields,
            "numIid": str(numIid),
            "timestamp": timestamp,
            "sign": ms
        }
        res = requests.post(url, data=data, headers=headers)
        json_html = res.text
        # 示例数据
        # {"IsSuccess":true,"Data":{"AfterSaleId":0,"ApproveStatus":null,"AuctionPoint":0,"AutoFill":null,"AutoRepost":false,"Barcode":null,"ChangeProp":null,"ChaoshiExtendsInfo":null,"ChargeFreeList":null,"Cid":0,"CodPostageId":0,"CpvMemo":null,"Created":null,"CuntaoItemSpecific":null,"CustomMadeTypeId":null,"DelistTime":null,"DeliveryTime":null,"Desc":null,"DescModuleInfo":null,"DescModules":null,"DetailUrl":null,"EmsFee":null,"ExpressFee":null,"Features":null,"FoodSecurity":null,"FreightPayer":null,"GlobalStockCountry":null,"GlobalStockDeliveryPlace":null,"GlobalStockTaxFreePromise":false,"GlobalStockType":null,"HasDiscount":false,"HasInvoice":false,"HasShowcase":false,"HasWarranty":false,"Iid":null,"Increment":null,"InnerShopAuctionTemplateId":0,"InputCustomCpv":null,"InputPids":null,"InputStr":null,"Is3D":false,"IsAreaSale":false,"IsCspu":false,"IsEx":false,"IsFenxiao":0,"IsLightningConsignment":false,"IsPrepay":false,"IsTaobao":false,"IsTiming":false,"IsVirtual":false,"IsXinpin":false,"ItemImgs":null,"ItemRectangleImgs":null,"ItemSize":null,"ItemWeight":null,"ItemWirelessImgs":null,"LargeScreenImageUrl":null,"ListTime":null,"LocalityLife":null,"Location":null,"Modified":null,"MpicVideo":null,"MsPayment":null,"Newprepay":"default","Nick":"金榜教育服务","Num":0,"NumIid":0,"O2oBindService":false,"OneStation":false,"OuterId":null,"OuterShopAuctionTemplateId":0,"PaimaiInfo":null,"PeriodSoldQuantity":0,"PicUrl":null,"PostFee":null,"PostageId":0,"Price":null,"ProductId":0,"PromotedService":null,"PropImgs":null,"PropertyAlias":null,"Props":null,"PropsName":null,"Qualification":null,"Score":0,"SecondKill":null,"SellPoint":null,"SellPromise":false,"SellerCids":null,"Skus":null,"SoldQuantity":0,"SpuConfirm":false,"StuffStatus":null,"SubStock":0,"SupportChargeFree":false,"TemplateId":null,"Title":null,"Type":"fixed","ValidThru":0,"VerticalImgs":null,"VideoId":0,"Videos":null,"Violation":false,"Volume":0,"WapDesc":null,"WapDetailUrl":null,"WhiteBgImage":null,"WirelessDesc":null,"WithHoldQuantity":0,"WwStatus":false},"Error_Code":0,"Error_Msg":"","AllowRetry":null}
        html = json.loads(json_html)
        IsSuccess = html['IsSuccess']
        if IsSuccess:
            nick = html['Data']['Nick']
            print('存储卖家信息,卖家信息是根据宝贝id来找到的，一个卖家对应多个宝贝,一个宝贝id对应一个卖家')
            jsonStr = {"result": nick}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
        jsonStr = {"result": "获取失败"}
        return HttpResponse(json.dumps(jsonStr), content_type="application/json")





