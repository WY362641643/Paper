from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import json
import time
from agency import modelsmiddleware as MDW
import os
from django.conf import settings
import random
import urllib.parse as up

# Create your views here.

source = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C',
          'V', 'B', 'N', 'M',
          'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'j', 'h', 'k', 'l', 'm', 'n', 'b',
          'v', 'c', 'x', 'z',
          '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
          ]


def index_views(request):
    if request.method == "GET":
        return render(request, 'cnkicn.html')


# 单篇上传
def cnki(request):
    if request.method == 'POST':
        ver_chktype = request.POST['ver_chktype']
        paper_title = request.POST['paper_title']  # 论文标题
        paper_author = request.POST['paper_author']  # 论文作者
        upload_file_name = request.POST['upload_file_name']  # 论文文件名称
        upload_file_tmpname = request.POST['upload_file_tmpname']
        upload_file_md5 = request.POST['upload_file_md5']
        paper_type = request.POST['paper_type']
        pay_type = request.POST['pay_type']
        device_id = request.POST['device_id']
        script_url = request.POST['script_url']
        orderId1 = request.POST['orderId1']
        if 'orderId2' in request.POST:
            orderId2 = request.POST['orderId2']
            orderId3 = request.POST['orderId3']
            # 查询成功后 把order 转换成元组,第 0 个元素是类型, 第 1个元素是点单号
            # 注意,需要返回 此订单号的代理商 accobj
            accobj, orderId1 = MDW.round_robin([orderId1, orderId2, orderId3])
        else:
            accobj = MDW.test_card(orderId1)
            if not accobj:
                jsonDict = {"status": False, "info": "检测卡错误", "data": []}
                return HttpResponse(json.dumps(jsonDict), content_type="application/json")
        suffix = upload_file_name.split(".")[-1]
        path = os.path.join(settings.BASE_DIR, 'static/file/{}'.format(upload_file_name))
        if 'docx' in suffix:
            text = MDW.filedocx(path)
        elif 'txt' in suffix:
            text = MDW.filetxt(path)
        else:
            text = MDW.filedoc(path)
        word_number_text = len(text)
        if not MDW.textLenOrder(word_number_text, orderId1[0]):
            jsonStr = {
                'status': 0,
                'info': '类型错误: 文章字符数过多,请选择其他系统类型'
            }
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
        taskid, iscode = MDW.post_jiance(accobj.account, paper_author, paper_title, text)
        if not taskid:
            jsonStr = {
                'status': 0,
                'info': '检测接口未打卡, 请联系客服'
            }
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
        status = MDW.addDetection(accobj, orderId1, paper_title, paper_author, taskid, iscode, path,
                                  word_number_text)
        if not status:
            jsonStr = {
                'status': 0,
                'info': '添加检测失败,'
            }
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
        MDW.updateorder(orderId1)
        if isinstance(orderId1, tuple):
            orderId1 = orderId1[1]
        MDW.gods_up(orderId1)
        jsonStr = {"status": 1, "info": '', 'data': {
            'tid': orderId1,
        }}
        return HttpResponse(json.dumps(jsonStr), content_type="application/json")


# 多篇文件上传 文件检测
def upload_file(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('paper_file')
        # 获取当前时间的时间戳
        timestr = ''.join(random.sample(source, 2))
        # 获取后缀
        suffix = file_obj.name.split(".")[-1]
        if suffix not in ['txt', 'doc', 'docx']:
            jsonDict = {
                'status': False,
                'info': '不能识别的文件类型'
            }
            return HttpResponse(json.dumps(jsonDict), content_type="application/json")
        # 获取程序需要写入的文件路径
        filename = timestr + file_obj.name
        path = os.path.join(settings.BASE_DIR, 'static/file/{}'.format(filename))
        # 根据路径打开指定的文件(二进制形式打开)
        f = open(path, 'wb+')
        # chunks将对应的文件数据转换成若干片段, 分段写入, 可以有效提
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        jsonDict = {"status": True, "info": "\u6210\u529f", "data": {
            "upload_file_name": filename,
            "upload_file_tmpname": "cnki\/914549304a7d607df76001167848b6aa.doc",
            "upload_file_md5": "6e47d76364d177d976318f10d3728220",
            "crypto_key": "P7YsAfeQ\/wgymEalC00CS0NEG9FloL9e+btjV92APSHz9GN7XOz1uIR76vAtZSiwiVwXl6SHIwR6oerZF5jUZwJbNo0Xo61z3BfEMzrZ7GxP4dfCSjjSkyTFXwOH+Qs3D0k3Dg1SVDUzaic1wuAvUQ==",
            "upload_file_wordnum": 3993}
                    }
        return HttpResponse(json.dumps(jsonDict), content_type="application/json")


#  多篇 上传 文件检测
def multiple_upload_file(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('paper_file')
        # 获取当前时间的时间戳
        timestr = ''.join(random.sample(source, 2))
        # 获取后缀
        try:
            author, title = file_obj.name.split('_')[-2:]
            suffix = file_obj.name.split(".")[-1]
            if suffix not in ['txt', 'doc', 'docx']:
                raise ValueError
        except:
            jsonDict = {
                'status': False,
                'info': '不能识别的文件类型'
            }
            return HttpResponse(json.dumps(jsonDict), content_type="application/json")
        # 获取程序需要写入的文件路径
        filename = timestr + file_obj.name
        path = os.path.join(settings.BASE_DIR, 'static/file/{}'.format(filename))
        # 根据路径打开指定的文件(二进制形式打开)
        f = open(path, 'wb+')
        # chunks将对应的文件数据转换成若干片段, 分段写入, 可以有效提
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        jsonDict = {"status": True, "info": "\u6210\u529f", "data": {
            "upload_file_name": filename,
            "upload_file_tmpname": "cnki\/914549304a7d607df76001167848b6aa.doc",
            "upload_file_md5": "6e47d76364d177d976318f10d3728220",
            "crypto_key": "P7YsAfeQ\/wgymEalC00CS0NEG9FloL9e+btjV92APSHz9GN7XOz1uIR76vAtZSiwiVwXl6SHIwR6oerZF5jUZwJbNo0Xo61z3BfEMzrZ7GxP4dfCSjjSkyTFXwOH+Qs3D0k3Dg1SVDUzaic1wuAvUQ==",
            "upload_file_wordnum": 3993}
                    }
        return HttpResponse(json.dumps(jsonDict), content_type="application/json")
# 检测淘宝订单号
def ajax_check_order(request):
    if request.method == 'GET':
        _ = request.GET.get('_')
        tid = request.GET.get('tid')
        status = MDW.select_order_account(tid)
        if status:
            jsonDict = {"status": True, "info": "订单号可用", "data": []}
        else:
            jsonDict = {"status": False,
                        "info": "来自淘宝的信息：订单号【" + str(
                            tid) + "】有误，可能是：订单次数使用完或商家类型数量不足,请联系客服",
                        "data": []}
        return HttpResponse(json.dumps(jsonDict), content_type="application/json")


# 多篇上传
def multiple(request):
    if request.method == 'GET':
        return render(request, 'multiple.html')
    else:
        ver_chktype = request.POST['ver_chktype']
        multiple = request.POST['multiple']
        upload_file_names = request.POST['upload_file_name']
        upload_file_tmpname = request.POST['upload_file_tmpname']
        upload_file_md5 = request.POST['upload_file_md5']
        paper_type = request.POST['paper_type']
        pay_type = request.POST['pay_type']
        orderId1 = request.POST['orderId1']
        device_id = request.POST['device_id']
        script_url = request.POST['script_url']
        if 'orderId2' in request.POST:
            orderId2 = request.POST['orderId2']
            orderId3 = request.POST['orderId3']
            # 查询成功后 把order 转换成元组,第 0 个元素是类型, 第 1个元素是点单号
            # 注意,需要返回 此订单号的代理商 accobj
            accobj, orderId1 = MDW.round_robin([orderId1, orderId2, orderId3])
            if not accobj:
                jsonDict = {"status": False, "info": "订单编号错误", "data": []}
                return HttpResponse(json.dumps(jsonDict), content_type="application/json")
        else:
            accobj = MDW.test_card(orderId1)
            if not accobj:
                jsonDict = {"status": False, "info": "检测卡错误", "data": []}
                return HttpResponse(json.dumps(jsonDict), content_type="application/json")
        for upload_file_name in upload_file_names.split(';'):
            if not upload_file_name:
                continue
            suffix = upload_file_name.split(".")[-1]
            author, title = upload_file_name.split('_')[-2:]
            path = os.path.join(settings.BASE_DIR, 'static/file/{}'.format(upload_file_name))
            if 'docx' in suffix:
                text = MDW.filedocx(path)
            elif 'txt' in suffix:
                text = MDW.filetxt(path)
            else:
                text = MDW.filedoc(path)
            word_number_text = len(text)
            if not MDW.textLenOrder(word_number_text, orderId1[0]):
                jsonStr = {
                    'status': 0,
                    'info': '类型错误: 文章字符数过多,请选择其他系统类型'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            taskid, iscode = MDW.post_jiance(accobj.account, author, title, text)
            if not taskid:
                jsonStr = {
                    'status': 0,
                    'info': '检测接口未打卡, 请联系客服'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            status = MDW.addDetection(accobj, orderId1, title, author, taskid, iscode, path, word_number_text)
            if not status:
                jsonStr = {
                    'status': 0,
                    'info': '添加检测失败,'
                }
                return HttpResponse(json.dumps(jsonStr), content_type="application/json")
            MDW.updateorder(orderId1)
            if isinstance(orderId1, tuple):
                orderId1 = orderId1[1]
            MDW.gods_up(orderId1)
            jsonStr = {"status": 1, "info": '', 'data': {
                'tid': orderId1,
            }}
        return HttpResponse(json.dumps(jsonStr), content_type="application/json")


# 下载检测报告
def report(request):
    if request.method == 'GET':
        order = request.GET.get('orderNum')
        # message = MDW.select_DetectionList_order(order)
        # if message:
        #     jsonDict = {
        #         'status':1,
        #         'info':'',
        #         'data':message
        #     }
        # else:
        #     jsonDict = {
        #         'status':1,
        #         'info':'',
        #         'data':message
        #     }
        return render(request, 'report.html')


# 下载检测报告
def download(request, order, id):
    if request.method == 'GET':
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


# 通过 订单编号 查看检测进程
def report_tid_order(request, order):
    if request.method == 'GET':
        order = {
            'order': order
        }
        return render(request, 'report.html', locals())


# 前端提交订单查询论文检测进度 之前 查询订单号是否正确
def ajax_search_order(request):
    if request.method == 'GET':
        tid = request.GET.get('tid')
        data = MDW.select_detec_order(tid)
        if data:
            jsonDic = {
                'status': True,
                'info': 0,
                'data': data
            }
        else:
            jsonDic = {
                'status': False,
                'info': 0,
                'data': data
            }
        return HttpResponse(json.dumps(jsonDic), content_type="application/json")
    else:
        # 这是广告请求
        jsonDic = {"status": True, "info": "get succ",
                   "data": {"uid": "1809", "domain": "jinbang.celunwen.com", "beian": "",
                            "sitename": "\u4e2d\u56fd\u77e5\u7f51\u8bba\u6587\u68c0\u6d4b\u67e5\u91cd\u7cfb\u7edf\u5165\u53e3-\u514d\u6ce8\u518c,24\u5c0f\u65f6\u5168\u81ea\u52a9\u68c0\u6d4b",
                            "sitekeywords": "\u77e5\u7f51\u5e10\u53f7\u3001\u6587\u732e\u4e0b\u8f7d\u3001\u77e5\u7f51\u67e5\u91cd,\u77e5\u7f51\u8bba\u6587\u67e5\u91cd\u5165\u53e3,\u77e5\u7f51\u8bba\u6587\u68c0\u6d4b,\u8bba\u6587\u68c0\u6d4b,\u8bba\u6587\u67e5\u91cd,\u77e5\u7f51\u8bba\u6587\u67e5\u91cd,\u77e5\u7f51\u8bba\u6587\u68c0\u6d4b\u7cfb\u7edf,\u77e5\u7f51\u8bba\u6587\u68c0\u6d4b\u5165\u53e3,cnki\u8bba\u6587\u68c0\u6d4b,\u7855\u58eb\u8bba\u6587\u68c0\u6d4b",
                            "sitedesc": "\u77e5\u7f51\u5e10\u53f7\u3001\u6587\u732e\u4e0b\u8f7d\u3001\u77e5\u7f51\u8bba\u6587\u68c0\u6d4b\u7cfb\u7edf\u662f\u6700\u6743\u5a01\u7684\u672c\u7855\u535a\u5b66\u4f4d\u8bba\u6587\u68c0\u6d4b\u7cfb\u7edf\uff0c\u7cfb\u7edf\u4ee5\u4e2d\u56fd\u5b66\u672f\u6587\u732e\u7f51\u7edc\u51fa\u7248\u603b\u5e93\u4e3a\u5168\u6587\u6bd4\u5bf9\u6570\u636e\u5e93\uff0c\u53ef\u68c0\u6d4b\u6284\u88ad\u4e0e\u527d\u7a83\u3001\u4f2a\u9020\u3001\u7be1\u6539\u7b49\u5b66\u672f\u4e0d\u7aef\u6587\u732e\uff0c\u53ef\u4f9b\u9ad8\u6821\u68c0\u6d4b\u5b66\u4f4d\u8bba\u6587\u548c\u5df2\u53d1\u8868\u7684\u8bba\u6587\u3002",
                            "access_stats_code": "", "company_name": "", "tbhome": "", "v_chknum": "36826681",
                            "phone_num": "", "wangwang": "", "qq": "845908664", "is_public_tpl": "1",
                            "short_name": "\u91d1\u699c\u6559\u80b2", "open_process": "5",
                            "regtime": "2019-02-01 21:14:01", "aid": "9", "miji_filename": "", "site_tpl": "2",
                            "is_open_fx": "0", "sale_channel": "0", "is_open_fx2": "0",
                            "fx2_open_time": "0000-00-00 00:00:00",
                            "service_domain": "http:\/\/jinbang.celunwen.com\/cnki"}}
        return HttpResponse(json.dumps(jsonDic), content_type="application/json")


# 1前端提交 删除 检测记录
def ajax_del_report(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        orderid = request.GET.get('tid')
        MDW.ajax_del_report(orderid, sid)
        jsonDic = {'status': True,
                   'info': '删除成功',
                   'data': []}
        return HttpResponse(json.dumps(jsonDic), content_type="application/json")
