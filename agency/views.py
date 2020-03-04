from django.shortcuts import render, redirect
from django.http import HttpResponse,FileResponse
from django.contrib.auth import authenticate
import json
import time
import os
from . import modelsmiddleware as MDW
from django.conf import settings
import requests
import urllib.parse as up
import zipfile
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
                timestr = str(time.time()).replace('.', '')
                filename = str(types)+'_'+str(author)+'_'+str(title)+'.txt'
                path = os.path.join(settings.BASE_DIR, 'static/file/{0}{1}'.format(timestr, filename))
                # 根据路径打开指定的文件
                with open(path, 'a',encoding='utf-8') as f:
                    f.write(fulltext)
                taskid,iscode = MDW.post_jiance(name,author,title,fulltext)
                MDW.addDetection(accobj, types, title, author, taskid, iscode,path)
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
                    'message': '文件命名规则错误'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            if len(order)==1:
                if not MDW.surplus_minus(accobj, order):
                    jsonStr = {
                        'result': 0,
                        'message': '此系统类型剩余次数不足'
                    }
                    return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            elif not MDW.orderisactivate(order):
                jsonStr = {
                    'result': 0,
                    'message': '检测卡错误或已激活'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            # 获取当前时间的时间戳
            timestr = str(time.time()).replace('.', '')
            # 获取程序需要写入的文件路径
            path = os.path.join(settings.BASE_DIR, 'static/file/{0}{1}'.format(timestr, file_obj.name))
            # 根据路径打开指定的文件(二进制形式打开)
            f = open(path, 'wb+')
            # chunks将对应的文件数据转换成若干片段, 分段写入, 可以有效提
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
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
            return HttpResponse('<h1>提交成功</h1>')
        else:
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
    return render(request, 'login.html')
# # 删除超过 15天的数据
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
        filename = up.quote("_".join(filepath.split('/')[-1].split('_')[1:]))
        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
        return response

# 批量下载前压缩
def zipDir(dirpath_list,outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zips = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    filenamelist=[]
    for filepath in dirpath_list:
        filenamelist.append(filepath.split('/')[-1])
    dpath = os.path.join(settings.BASE_DIR, 'static/file/')
    for filename in filenamelist:
        zips.write(os.path.join(dpath,filename),os.path.join('',filename))
    zips.close()

# 批量下载文件
def batchDownload(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        ids = request.GET.get('ids')
        idls = ids.split(',')
        filepathlist =[]
        for id in idls:
            if id:
                filepathlist.append(MDW.selectfilepath(id))
        timestr = str(time.time()).replace('.', '')
        zippath = os.path.join(settings.BASE_DIR, 'static/zipfiles/{0}{1}'.format(timestr, '.zip'))
        zipDir(filepathlist,zippath)
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


# 打包文档
def docpack(request):
    if 'sname' in request.session:
        name = request.session['sname']
        pwd = request.session['spwd']
        accobj = MDW.account_result(name, pwd)
        if not accobj:
            return render(request, 'login.html')
        if request.method == 'GET':
            return render(request, 'doc.html', locals())
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
            jsonStr = {"result": 1, "msg": ''}
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
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
            return render(request, 'product.html', locals())
        else:
            jsonStr = {"result": 1, "msg": ''}
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
