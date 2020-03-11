from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import json
import time
from agency import modelsmiddleware as MDW
import os
from django.conf import settings
import random

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
        paper_author = request.POST['paper_author'] # 论文作者
        upload_file_name = request.POST['upload_file_name'] # 论文文件名称
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
            accobj,orderId1 = MDW.round_robin([orderId1,orderId2,orderId3])
        else:
            accobj = MDW.test_card(orderId1)
            if not accobj:
                jsonDict= {"status": True, "info": "检测卡错误", "data": []}
                return HttpResponse(json.dumps(jsonDict), content_type="application/json")
        suffix = upload_file_name.split(".")[-1]
        path = os.path.join(settings.BASE_DIR, 'static/cnkifile/{}'.format(upload_file_name))
        if suffix == 'docx':
            text = MDW.filedocx(path)
        elif suffix == 'txt':
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
        if not MDW.addDetection(accobj, orderId1, paper_title, paper_author, taskid, iscode, path, word_number_text):
            jsonStr = {
                'status': 0,
                'info': '添加检测失败,'
            }
            return HttpResponse(json.dumps(jsonStr), content_type="application/json")
        MDW.updateorder(orderId1)
        jsonStr = {"status": 1, "info": '','data':{
            'tid':'订单编号查询状态'
        }}
        return HttpResponse(json.dumps(jsonStr), content_type="application/json")
# 单篇上传 文件检测
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
        filename = timestr+file_obj.name
        path = os.path.join(settings.BASE_DIR, 'static/cnkifile/{}'.format(filename))
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

# 单篇上传 检测淘宝订单号
def ajax_check_order(request):
    if request.method == 'GET':
        _ = request.GET.get('_')
        tid = request.GET.get('tid')
        status = MDW.ajax_check_order(tid)
        if status:
            jsonDict = {"status":True,"info":"订单号可用","data":[]}
        else:
            jsonDict = {"status": False,
             "info": "来自淘宝的信息：订单号【1234567891234】有误，可能是：Invalid session:非法或过期的SessionKey参数，请使用有效的SessionKey参数",
             "data": []}
        return HttpResponse(json.dumps(jsonDict), content_type="application/json")
# 多篇上传
def multiple(request):
    if request.method == 'GET':
        return render(request,'multiple.html')
# 下载检测报告
def report(request):
    if request.method == 'GET':
        return render(request,'report.html')
