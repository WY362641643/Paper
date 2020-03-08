#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/3 11:33
# @Author  : 亦轩
# @File    : 111.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2i
import json
import datetime
import random
import re

with open('templates/CheckResult.json','r',encoding='utf-8')as f:
    restext = f.read()
resDict = json.loads(restext)
source = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0','1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
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
A_body='''<div class="n_xu">
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
paragraph_text ='''<div class="n_bodymid_ywnr" id="Repeater1_ctl00_Red_Content">
    <table width="640" class="n_table_ywtop" border="0" cellspacing="0" cellpadding="0">
        <tbody>
        <tr>
            <td height="26" class="n_ywnr">原文内容</td>
        </tr>
        </tbody>
    </table>
    <div class="n_ywnr_content" style="-ms-word-break: break-all; -ms-word-wrap: break-word;">{paragraph_text}</div>
</div>'''
paragraph_qwdz = ''''''
# 剽窃头
plagiarize_head = '<div id="Repeater1_ctl00_Standard_Content" class="n_ymnr_bz"><div class="n_ymnr_top">指&nbsp;&nbsp;&nbsp;&nbsp;标</div><div class="n_ymnr_top_s"><table cellpadding="0" cellspacing="0" border="0" width="620" class="n_table_bz"></table><table cellpadding="0" cellspacing="0" border="0" width="620" class="n_table_bz"><tbody><tr><td class="n_table_bz_gdh" colspan="2">疑似剽窃文字表述</td>'
# 剽窃数据
plagiarize_data = '''<tr>
                <td class="n_table_bz_mark" width="25" style="vertical-align: top;">
                    {index}.
                </td>
                <td class="n_table_bz_gd">
                    {text}
                   </td>
            </tr>'''
# 剽窃结尾
plagiarize_food = '''</tbody>
        </table>
    </div>
</div>'''
def reference(ruselt):
    if ruselt:
        return '是'
    return '否'
# 检测报告 与 相似文献列表
paragraph_list  = []  #　存放各个部分的数据
quanwenbiaominyinyong ='' # 全文标明引用
for paragraph in resDict['report_annotation_ref']['chapters']:
    paragraph_head ={
        'paragraph_chapter':paragraph['chapter'],
        'paragraph_word_count':paragraph['word_count'],
        'paragraph_similarity':str(float('%.4f' % (float(paragraph['similarity'])*100))) + '%',
            }
    paragraphtd = A_head.format(**paragraph_head)
    body_list = paragraph['sources']
    for index in range(int(len(body_list)/3)):
        body = body_list[index]
    # for index,body in enumerate(paragraph['sources']):
        try:
            paragraph_body = {
                'paragraph_reference':reference(body['reference']),
                'paragraph_similarity':str(float('%.4f' % (float(body['similarity'])*100))) + '%',
                'paragraph_source':body['source'],
                'paragraph_title':body['title'],
                'paragraph_year':body['year'],
                'index':index + 1,
            }
            paragraphtd += A_body.format(**paragraph_body)
        except:
            continue
    paragraphtd +='</div>'
    # A 系统的全文标明引用报告
    paragraph_list.append(paragraphtd)
    text = paragraph['text']
    plagiarize = re.findall(r'<em.*?</em>',text,flags=re.S)
    quanwenbiaominyinyong += paragraphtd + paragraph_text.format(paragraph_text=text) + plagiarize_head
    plagiarizes = ''
    for index in range(int(len(plagiarize)/3)):
        msg = {
            'index':index+1,
            'text':plagiarize[index]
        }
        plagiarizes += plagiarize_data.format(**msg)
    quanwenbiaominyinyong += plagiarizes + plagiarize_food
paragraph_ywnr_head = '''<tbody>
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
paragraph_ywnr = '''<tr>
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
paragraph_xsnrly = '''<tr>
                        <td class="n_bgd_biao_c"> {text}&nbsp;&nbsp;&nbsp;&nbsp;{author}-《{title}》-{year}（是否引证：
                            <span class="n_text_yz">{reference}</span>）
                        </td>
                    </tr>'''
quanwenduizhao = ''
for index,paragraph in enumerate(resDict['report_fulltext_comparison']['chapters']):
    paragraphtd =paragraph_ywnr_head
    similar_paragraph_list = paragraph['similar_paragraphs']
    paragraph_refer_row = ''
    i = 1
    for index_child in range(int(len(similar_paragraph_list)/3)):
    # for similar_paragraphs in paragraph['similar_paragraphs']:
        similar_paragraphs = similar_paragraph_list[index_child]
        paragraph_table = {
                'similar_word_count':similar_paragraphs['similar_word_count'],
                'text':similar_paragraphs['text'],
                'index':i,
        }
        paragraph_refer = paragraph_ywnr.format(**paragraph_table)
        paragraph_child = ''
        for sources in similar_paragraphs['sources']:
            try:
                sources_table ={
                    'text':sources['text'],
                    'reference':sources['reference'],
                    'year':sources['year'],
                    'author':sources['author'],
                    'title':sources['title'],
                }
                paragraph_child += paragraph_xsnrly.format(**sources_table)
            except:
                continue
        if paragraph_child:
            paragraph_refer += paragraph_child + '</tbody></table></td></tr>'
            i += 1
        else:
            continue
        paragraph_refer_row += paragraph_refer

    quanwenduizhao += paragraph_list[index] + paragraphtd + paragraph_refer_row + '</tbody></table></div></tbody>'
n_table_a_child ='''<TR>
    <TD width="20" height="25">&nbsp;                                    </TD>
    <TD style="width: 58px; text-align: left;">
      <DIV class="per_y">{similarity}</DIV></TD>
    <TD width="50" align="left">({word_similar_count})                                     </TD>
    <TD class="n_text_block_a2"><A href=""> 
                                                 {chapter}</A> （总{word_count}字）  
                                         </TD></TR>'''
n_table_a ='<TABLE class="n_table_a" border="0" cellspacing="0" cellpadding="0"><TBODY>'
for paragraph in resDict['report_fulltext_comparison']['chapters']:
    msg ={
        "chapter":paragraph["chapter"],
        "word_count":paragraph['word_count'],
        "similarity":str(float('%.4f' % (float(paragraph["similarity"])*100))) + '%',
        "word_similar_count":paragraph["word_similar_count"]
    }
    n_table_a += n_table_a_child.format(**msg)
n_table_a +='</TBODY></TABLE>'
similarity = float('%.4f' % (float(resDict['similarity'])*100))
no_problem = 100 - similarity
article_copy =100 - no_problem
message = {
    'article_copy':article_copy,  # 文章复制部分
    'no_problem':no_problem,  # 无问题部分
    'n_table_a':n_table_a,  # 论文各部分数据总汇
    'Detection_of_the_literature':resDict['title'],  # 检测文献标题
    'title_type':'全文对照',
    'similarity':str(similarity) + '%',  # 总文字复制比 去除引用文献复制比 去除本人已发表文献复制比 文字复制比
    'source_max_similar_similarity':resDict['source_max_similar_similarity'],  # 单篇最大文字复制比
    'report_fulltext_comparison_word_similar_count':resDict['report_fulltext_comparison']['word_similar_count'],  # 重复字数
    'word_count':resDict['word_count'],      # 总字数
    'source_max_similar_count':resDict['source_max_similar_count'], # 单篇最大重复字数
    'chapter_count':resDict['chapter_count'],       #   总段落数
    'report_annotation_ref_front_part_similar_count':resDict['report_annotation_ref']['front_part_similar_count'],  # 前部重合字数
    'report_annotation_ref_chapter_max_similar_word_count':resDict['report_annotation_ref']['chapter_max_similar_word_count'], # 疑似段落最大重复字数
    'report_annotation_ref_chapter_similar_count':resDict['report_annotation_ref']['chapter_similar_count'],  # 疑似段落数
    'report_annotation_ref_last_part_similar_count':resDict['report_annotation_ref']['last_part_similar_count'],  # 后部重合字数
    'report_annotation_ref_chapter_min_similar_word_count':resDict['report_annotation_ref']['chapter_min_similar_word_count'],  # 疑似段落最小重复字数
    'author':resDict['author'],  # 作者
    'number_date':datetime.datetime.now().strftime('%Y%m%d'),  # 编号上的时间
    'test_time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 检测时间
    'number_random':''.join(random.sample(source, 12)),  # 编号上的随机数
    'range_time':datetime.datetime.now().strftime('%Y-%m-%d'),
'paragraphtd':quanwenduizhao, # 文章对比数据
}
with open('templates/reprot/A1.html','r',encoding='utf-8')as f:
    html = f.read()
html = re.sub('{','￥$',html,flags=re.S)
html = re.sub('}','￥',html,flags=re.S)
html = re.sub('~','{',html,flags=re.S)
html = re.sub('\^','}',html,flags=re.S)
htmlqwdz = html.format(**message)
htmlqwdz = re.sub('￥\$','{',htmlqwdz,flags=re.S)
htmlqwdz = re.sub('￥','}',htmlqwdz,flags=re.S)
with open('A-全文对照.html','w',encoding='utf-8')as f:
    f.write(htmlqwdz)
message['paragraphtd'] = quanwenbiaominyinyong
message['title'] = '全文标明引文'
htmlqwbmyy = html.format(**message)
htmlqwbmyy = re.sub('￥\$','{',htmlqwbmyy,flags=re.S)
htmlqwbmyy = re.sub('￥','}',htmlqwbmyy,flags=re.S)
with open('A-全文标明引用.html','w',encoding='utf-8')as f:
    f.write(htmlqwbmyy)