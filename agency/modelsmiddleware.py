#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/2/29 23:22
# @Author  : 亦轩
# @File    : modelsmiddleware.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2

from django.conf import settings
from .models import *
from win32com import client as wc
import time
import docx
import requests
import json
import datetime
import random
import re
import os
import zipfile
from urllib import parse as up
source = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
]
A_head = '''<div class="n_bodymid_bf">
    <table width="640" class="n_table_jiebf" border="0" cellspacing="0" cellpadding="0">
        <tbody>
        <tr>
            <td width="25" height="30" class="n_bf_bt"></td>
            <td width="499" class="n_text_block_bs"><a name="34255109_000"></a>{paragraph_chapter}</td>
            <td width="116" class="n_table_jiebf_zzs">总字数： <span class="n_text_block_bs">{paragraph_word_count}</span>
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <table width="640" class="n_table_jiebfs" border="0" cellspacing="0" cellpadding="0">
                    <tbody>
                    <tr>
                        <td width="90" style="text-indent: 1em;">相似文献列表</td>
                        <td width="150" class="n_table_jiebf_fzb">文字复制比：</td>
                        <td width="100">
                            <div class="n_jcjg_am">{paragraph_similarity}</div>
                        </td>
                        <td class="n_table_jiebf_fzb" style="text-align: left;">疑似剽窃观点（0）</td>
                    </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        </tbody>
    </table>'''
A_body = '''<div class="n_xu">
        <table class="n_table_a" border="0" cellspacing="0" cellpadding="0">
            <tbody>
            <tr>
                <td width="20" class="n_xu_a n_text_back_a">{index}</td>
                <td width="500" class="n_text_G2"><a href="http://www.cnki.net" target="_blank">{paragraph_title}</a>
                </td>
                <td width="100" class="n_xu_d n_text_red_d">{paragraph_similarity}</td>
            </tr>
            <tr>
                <td></td>
                <td class="n_text_block_b"> - 《{paragraph_source}》- {paragraph_year}</td>
                <td width="100" class="n_xu_da">是否引证： <span class="n_text_yz">{paragraph_reference}</span></td>
            </tr>
            </tbody>
        </table>
    </div>'''
A_paragraph_text = '''<div class="n_bodymid_ywnr" id="Repeater1_ctl00_Red_Content">
    <table width="640" class="n_table_ywtop" border="0" cellspacing="0" cellpadding="0">
        <tbody>
        <tr>
            <td height="26" class="n_ywnr">原文内容</td>
        </tr>
        </tbody>
    </table>
    <div class="n_ywnr_content" style="-ms-word-break: break-all; -ms-word-wrap: break-word;">{paragraph_text}</div>
</div>'''
# 剽窃头
A_plagiarize_head = '<div id="Repeater1_ctl00_Standard_Content" class="n_ymnr_bz"><div class="n_ymnr_top">指&nbsp;&nbsp;&nbsp;&nbsp;标</div><div class="n_ymnr_top_s"><table cellpadding="0" cellspacing="0" border="0" width="620" class="n_table_bz"></table><table cellpadding="0" cellspacing="0" border="0" width="620" class="n_table_bz"><tbody><tr><td class="n_table_bz_gdh" colspan="2">疑似剽窃文字表述</td>'
# 剽窃数据
A_plagiarize_data = '''<tr>
                <td class="n_table_bz_mark" width="25" style="vertical-align: top;">
                    {index}.
                </td>
                <td class="n_table_bz_gd">
                    {text}
                   </td>
            </tr>'''
# 剽窃结尾
A_plagiarize_food = '''</tbody>
        </table>
    </div>
</div>'''
A_paragraph_ywnr_head = '''<tbody>
<div class="n_qwdz_ywnr">
    <table border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; table-layout: fixed;"
           id="table2" class="n_bgd_biao">
        <tbody>
        <tr id="Repeater1_ctl00_tr_item">
            <td class="n_bgd_biao_b" width="330" colspan="2">原文内容
            </td>
            <td width="310" class="n_bgd_biao_bs">相似内容来源
            </td>
        </tr>
        </tbody>
    </table>
    <table border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; table-layout: fixed;"
           id="table3" class="n_bgd_biao">
        <tbody>'''
A_paragraph_ywnr = '''<tr>
            <td class="n_table_xu_a">
                {index}
            </td>
            <td class="n_bgd_biao_KU" style="vertical-align: top; width: 309px;">
                <div class="n_text_red_ax">
                    此处有&nbsp;{similar_word_count}&nbsp;字相似
                </div>
                <div class="n_bgd_biao_KUa n_red huanhang">{text}</div>
            </td><td class="n_bgd_biao_KU" style="vertical-align: top; width: 310px;">
                <table>
                    <tbody>'''
A_paragraph_xsnrly = '''<tr>
                        <td class="n_bgd_biao_c"> {text}&nbsp;&nbsp;&nbsp;&nbsp;{author}-《{title}》-{year}（是否引证：
                            <span class="n_text_yz">{reference}</span>）
                        </td>
                    </tr>'''
n_table_a_child = '''<TR>
    <TD width="20" height="25">&nbsp;                                    </TD>
    <TD style="width: 58px; text-align: left;">
      <DIV class="per_y">{similarity}</DIV></TD>
    <TD width="50" align="left">({word_similar_count})                                     </TD>
    <TD class="n_text_block_a2"><A href=""> 
                                                 {chapter}</A> （总{word_count}字）  
                                         </TD></TR>'''
# 论文检测接口
url = 'http://api.cnkin.net'
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
    data = {
        'appid': name,
        'author': author,
        'title': title,
        'content': fulltext,
    }
    try:
        res = requests.post(url+'/post/', data=data).text
        resdata = json.loads(res)
        if resdata['result'] == '1':
            taskid = resdata['returnval']
            iscode = 1
            return taskid,iscode
    except:
        pass
    # 送论文检测错误
    return '',-2
# 查询论文检测结果
def post_examiningz_report(id,state=False):
    '''
    查询论文检测结果
    :param id: 论文检测ID
    :param state:  是否重新打包
    :return:
    '''
    obj = DetectionList.objects.get(id=id)
    if obj.zipurl and not state:
        return obj.zipurl
    else:
        if obj.zipurl:
            original_path = obj.zipurl
            if os.path.exists(original_path):
                os.remove(original_path)
        data ={
            'appid':obj.account,
            'taskid':obj.taskid,
        }
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        res = requests.post(url + '/query/',headers=headers,data=data)
        if res.status_code != 200:
            print('接口错误')
            return False
        data = json.loads(res.text)['checkResult']
        accobj = obj.account
        advertpathobjlist = accobj.packdocument_set.all()
        advertpath_list = []
        for advert_path_obj in advertpathobjlist:
            advertpath_list.append(advert_path_obj.filename)
        zippath = Areport(data,advertpath_list)
        obj.zipurl=zippath
        obj.save()
        return zippath
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
# 查询账户剩余积分是否够用
def surplus_shengyu(accobj, surp):
    '''
    查询账户剩余积分是否够用
    :param account:
    :param surp:
    :return:
    '''
    accountSurplus_obj = Surplus.objects.get(account=accobj)
    if "A" in surp:
        if accountSurplus_obj.a <= 0:
            return False
    elif 'P' in surp:
        if accountSurplus_obj.p <= 0:
            return False
    elif 'V' in surp:
        if accountSurplus_obj.v <= 0:
            return False
    return True
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
# 处理 doc 文档
def filedoc(path):
    '''
    处理 doc 文档 返回文章字符串
    先将 doc 文档转换成 docx 文档
    再调用docx 文件读取文档
    :param path:
    :return:
    '''
    # word = wc.Dispatch("Word.Application")
    # doc = word.Documents.Open(path)
    # # 上面的地方只能使用完整绝对地址，相对地址找不到文件，且，只能用“\\”，不能用“/”，哪怕加了 r 也不行，涉及到将反斜杠看成转义字符。
    # doc.SaveAs(r"F:\\***\\***\\appendDoc\\***.docx", 12, False, "", True, "", False, False, False,False)  # 转换后的文件,12代表转换后为docx文件
    # # doc.SaveAs(r"F:\\***\\***\\appendDoc\\***.docx", 12)#或直接简写
    # # 注意SaveAs会打开保存后的文件，有时可能看不到，但后台一定是打开的
    # doc.Close
    # word.Quit
    word = wc.Dispatch('Word.Application')
    # 上面的地方只能使用完整绝对地址，相对地址找不到文件，且，只能用“\\”，不能用“/”，哪怕加了 r 也不行，涉及到将反斜杠看成转义字符。
    doc = word.Documents.Open(path)  # 目标路径下的文件
    path_package = path.split('.')
    docxpath = '.'.join(path_package[:-1]) + '.docx'
    doc.SaveAs(docxpath, 12, False, "", True, "", False, False, False, False)  # 转换后的文件,12代表转换后为docx文件
    doc.Close()
    try:
        word.Quit()
    except AttributeError:
        print('关闭 word 文件错误')
    text = filedocx(docxpath)
    # 删除 docx 文件
    if os.path.exists(docxpath):
        os.remove(docxpath)
    return text
# 处理docx文档
def filedocx(path):
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
# 处理txt文档
def filetxt(path):
    '''
    处理 text 文档 返回文章字符串
    :param path:
    :return:
    '''
    with open(path,'r') as f:
        text = f.read()
    return text
# 处理 wps 文档
def filewps(path):
    '''
    处理 text 文档 返回文章字符串
    :param path:
    :return:
    '''
    with open(path,'r') as f:
        text = f.read()
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
    if  'A' in order:
        if numbtext <= 50000:
            flag = True
    elif 'P' in order:
        if numbtext <= 150000:
            flag = True
    elif 'V' in order:
        if numbtext <= 250000:
            flag = True
    return flag
# 增加检测列表
def addDetection(accobj,order,title,author,taskid,iscode,path,number_text:int):
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
        obj.textnumber = number_text
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
    try:
        obj = DetectionList.objects.get(id=ids,iscode=-2,account=accobj)
        name = accobj.account
        author = obj.author
        title = obj.title
        filepath = obj.filepath
        if 'docx' in filepath.split('.'[-1]):
            fulltext = filedocx(filepath)
        else:
            with open(filepath,'r') as f:
                fulltext = f.read()
        taskid,iscode = post_jiance(name,author,title,fulltext)
        obj.taskid = taskid
        obj.iscode = iscode
        obj.date = round(time.time() * 1000)
        obj.save()
    except:
        pass
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
# 删除 15 天以后的数据
def deletedata15day(id):
    try:
        obj = DetectionList.objects.get(id=id)
        filepath = obj.filepath
        if os.path.exists(filepath):
            os.remove(filepath)
        zipurl = obj.zipurl
        if os.path.exists(zipurl):
            os.remove(zipurl)
        obj.delete()
    except:
        pass
# 批量下载前压缩
def zipDir(dirpath_list,path,outFullName,advertpath_list=''):
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
    dpath = os.path.join(settings.BASE_DIR, path)
    for filename in filenamelist:
        zips.write(os.path.join(dpath,filename),os.path.join('',filename))
    # 添加广告
    if advertpath_list:
        path = 'static/advertfile'
        filenamelist = []
        for filepath in advertpath_list:
            filenamelist.append(filepath.split('/')[-1])
        dpath = os.path.join(settings.BASE_DIR, path)
        for filename in filenamelist:
            zips.write(os.path.join(dpath, filename), os.path.join('', filename))
    zips.close()
# 生成 A系统的检测报告
def Areport(resDict,advertpath_list=''):
    timestr = str(resDict['title'].split('.')[0]) + '_' + ''.join(random.sample(source, 2))
    path = os.path.join(settings.BASE_DIR, 'static/report/{0}'.format(timestr))
    def reference(ruselt):
        if ruselt:
            return '是'
        return '否'
    # 检测报告 与 相似文献列表
    paragraph_list = []  # 存放各个部分的数据
    quanwenbiaominyinyong = ''  # 全文标明引用
    source_max_similar_title = ''  # 单片最大复制文章名称
    source_max = 0  # 单片最大复制文章分数
    for paragraph in resDict['report_annotation_ref']['chapters']:
        paragraph_head = {
            'paragraph_chapter': paragraph['chapter'],
            'paragraph_word_count': paragraph['word_count'],
            'paragraph_similarity': str(float('%.4f' % (float(paragraph['similarity']) * 100))) + '%',
        }
        paragraphtd = A_head.format(**paragraph_head)
        body_list = paragraph['sources']
        for index in range(int(len(body_list) / 3)):
            body = body_list[index]
            if body["similarity"] > source_max:
                source_max = body["similarity"]
                source_max_similar_title = body['title']
            try:
                paragraph_body = {
                    'paragraph_reference': reference(body['reference']),
                    'paragraph_similarity': str(float('%.4f' % (float(body['similarity']) * 100))) + '%',
                    'paragraph_source': body['source'],
                    'paragraph_title': body['title'],
                    'paragraph_year': body['year'],
                    'index': index + 1,
                }
                paragraphtd += A_body.format(**paragraph_body)
            except:
                continue
        paragraphtd += '</div>'
        # A 系统的全文标明引用报告
        paragraph_list.append(paragraphtd)
        text = paragraph['text']
        plagiarize = re.findall(r'<em.*?</em>', text, flags=re.S)
        quanwenbiaominyinyong += paragraphtd + A_paragraph_text.format(paragraph_text=text) + A_plagiarize_head
        plagiarizes = ''
        for index in range(int(len(plagiarize) / 3)):
            msg = {
                'index': index + 1,
                'text': plagiarize[index]
            }
            plagiarizes += A_plagiarize_data.format(**msg)
        quanwenbiaominyinyong += plagiarizes + A_plagiarize_food
    quanwenduizhao = ''
    for index, paragraph in enumerate(resDict['report_fulltext_comparison']['chapters']):
        paragraphtd = A_paragraph_ywnr_head
        similar_paragraph_list = paragraph['similar_paragraphs']
        paragraph_refer_row = ''
        i = 1
        for index_child in range(int(len(similar_paragraph_list) / 3)):
            # for similar_paragraphs in paragraph['similar_paragraphs']:
            similar_paragraphs = similar_paragraph_list[index_child]
            paragraph_table = {
                'similar_word_count': similar_paragraphs['similar_word_count'],
                'text': similar_paragraphs['text'],
                'index': i,
            }
            paragraph_refer = A_paragraph_ywnr.format(**paragraph_table)
            paragraph_child = ''
            for sources in similar_paragraphs['sources']:
                try:
                    sources_table = {
                        'text': sources['text'],
                        'reference': sources['reference'],
                        'year': sources['year'],
                        'author': sources['author'],
                        'title': sources['title'],
                    }
                    paragraph_child += A_paragraph_xsnrly.format(**sources_table)
                except:
                    continue
            if paragraph_child:
                paragraph_refer += paragraph_child + '</tbody></table></td></tr>'
                i += 1
            else:
                continue
            paragraph_refer_row += paragraph_refer

        quanwenduizhao += paragraph_list[index] + paragraphtd + paragraph_refer_row + '</tbody></table></div></tbody>'
    n_table_a = '<TABLE class="n_table_a" border="0" cellspacing="0" cellpadding="0"><TBODY>'
    for paragraph in resDict['report_fulltext_comparison']['chapters']:
        msg = {
            "chapter": paragraph["chapter"],
            "word_count": paragraph['word_count'],
            "similarity": str(float('%.4f' % (float(paragraph["similarity"]) * 100))) + '%',
            "word_similar_count": paragraph["word_similar_count"]
        }
        n_table_a += n_table_a_child.format(**msg)
    n_table_a += '</TBODY></TABLE>'
    similarity = float('%.4f' % (float(resDict['similarity']) * 100))
    no_problem = 100 - similarity
    article_copy = 100 - no_problem
    message = {
        'n_table_a': n_table_a,  # 论文各部分数据总汇
        'Detection_of_the_literature': resDict['source_max_similar_title'],  # 检测文献标题
         'title_type':'全文对照',
        'similarity': str(similarity) + '%',
    # 总文字复制比 去除引用文献复制比 去除本人已发表文献复制比 文字复制比
        'source_max_similar_similarity': resDict['source_max_similar_similarity'],  # 单篇最大文字复制比
        'report_fulltext_comparison_word_similar_count': resDict['report_fulltext_comparison']['word_similar_count'],
    # 重复字数
        'word_count': resDict['word_count'],  # 总字数
        'source_max_similar_count': resDict['source_max_similar_count'],  # 单篇最大重复字数
        'source_max_similar_title': source_max_similar_title,  # 单篇最大文字复制比标题
        'chapter_count': resDict['chapter_count'],  # 总段落数
        'report_annotation_ref_front_part_similar_count': resDict['report_annotation_ref']['front_part_similar_count'],
    # 前部重合字数
        'report_annotation_ref_chapter_max_similar_word_count': resDict['report_annotation_ref'][
            'chapter_max_similar_word_count'],  # 疑似段落最大重复字数
        'report_annotation_ref_chapter_similar_count': resDict['report_annotation_ref']['chapter_similar_count'],
    # 疑似段落数
        'report_annotation_ref_last_part_similar_count': resDict['report_annotation_ref']['last_part_similar_count'],
    # 后部重合字数
        'report_annotation_ref_chapter_min_similar_word_count': resDict['report_annotation_ref'][
            'chapter_min_similar_word_count'],  # 疑似段落最小重复字数
        'author': resDict['author'],  # 作者
        'number_date': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),  # 编号上的时间
        'test_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 检测时间
        'number_random': ''.join(random.sample(source, 12)),  # 编号上的随机数
        'range_time': datetime.datetime.now().strftime('%Y-%m-%d'),
        'paragraphtd': quanwenduizhao,  # 文章对比数据
    }
    with open('templates/reprot/A.html', 'r', encoding='utf-8')as f:
        html = f.read()
    html = re.sub('{', '￥$', html, flags=re.S)
    html = re.sub('}', '￥', html, flags=re.S)
    html = re.sub('~', '{', html, flags=re.S)
    html = re.sub('\^', '}', html, flags=re.S)
    htmlqwdz = html.format(**message)
    htmlqwdz = re.sub('￥\$', '{', htmlqwdz, flags=re.S)
    htmlqwdz = re.sub('￥', '}', htmlqwdz, flags=re.S)
    qwdz = path + 'A-全文对照.html'
    with open(qwdz, 'w', encoding='utf-8')as f:
        f.write(htmlqwdz)
    message['paragraphtd'] = quanwenbiaominyinyong
    message['title'] = '全文标明引文'
    htmlqwbmyy = html.format(**message)
    htmlqwbmyy = re.sub('￥\$', '{', htmlqwbmyy, flags=re.S)
    htmlqwbmyy = re.sub('￥', '}', htmlqwbmyy, flags=re.S)
    qwbmyy = path + 'A-全文标明引用.html'
    with open(qwbmyy, 'w', encoding='utf-8')as f:
        f.write(htmlqwbmyy)
    zippath = os.path.join(settings.BASE_DIR, 'static/zipfiles/{0}{1}'.format(timestr, '.zip'))
    zipDir([qwbmyy,qwdz],'static/report/', zippath,advertpath_list)
    if os.path.exists(qwdz):
        os.remove(qwdz)
    if os.path.exists(qwbmyy):
        os.remove(qwbmyy)
    return zippath
# 增加 广告 文档
def addpack(filename,accobj):
    try:
        obj = Packdocument()
        obj.account = accobj
        obj.filename = filename
        obj.save()
        return True
    except:
        return False
# 查看 广告 文档
def create(accobj):
    obj = Packdocument.objects.filter(account=accobj)
    msg = []
    for info in obj:
        msg.append(info.dic())
    return msg
# 删除广告文档
def deletdoc(accobj,ids):
    try:
        if isinstance(ids,list):
            for id in ids:
                if id:
                    obj = Packdocument.objects.get(account=accobj,id=id)
                    filename = obj.filename
                    filepath = os.path.join(settings.BASE_DIR, 'static/advertfile/{}'.format(filename))
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    obj.delete()
        else:
            obj = Packdocument.objects.get(account=accobj, id=ids)
            filename = obj.filename
            filepath = os.path.join(settings.BASE_DIR, 'static/file/'.format(filename))
            if os.path.exists(filepath):
                os.remove(filepath)
            obj.delete()
        return True
    except:
        return False
if __name__ == '__main__':
    filepath = 'C:\\Users\\Administrator\\Desktop\\project\\individual_event\\pdf_collect_porject\\Paper\\static\\file\A.doc'
    text = filedoc(filepath)
    print(text)