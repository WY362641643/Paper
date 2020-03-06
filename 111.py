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
n_bodymid_bf_head = '''<div class="n_bodymid_bf">
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
n_bodymid_bf_body='''<div class="n_xu">
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
paragraphtd = ''

def reference(ruselt):
    if ruselt:
        return '是'
    return '否'
for paragraph in resDict['report_annotation_ref']['chapters']:
    paragraph_head ={
        'paragraph_chapter':paragraph['chapter'],
        'paragraph_word_count':paragraph['word_count'],
        'paragraph_similarity':str(float('%.4f' % (float(paragraph['similarity'])*100))) + '%',
            }
    paragraphtd += n_bodymid_bf_head.format(**paragraph_head)
    for index,body in enumerate(paragraph['sources']):
        try:
            paragraph_body = {
                'paragraph_reference':reference(body['reference']),
                'paragraph_similarity':str(float('%.4f' % (float(body['similarity'])*100))) + '%',
                'paragraph_source':body['source'],
                'paragraph_title':body['title'],
                'paragraph_year':body['year'],
                'index':index + 1,
            }
            paragraphtd += n_bodymid_bf_body.format(**paragraph_body)
        except:
            continue
    paragraphtd +='</div>'
    paragraphtd +=paragraph_text.format(paragraph_text=paragraph['text'])

message = {
    'similarity':str(float('%.4f' % (float(resDict['similarity'])*100))) + '%',  # 总文字复制比 去除引用文献复制比 去除本人已发表文献复制比 文字复制比
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
    'test_time':resDict['time'],  # 检测时间
    'number_random':''.join(random.sample(source, 12)),  # 编号上的随机数
    'paragraphtd':paragraphtd, # 文章对比数据
}

with open('templates/reprot/A_yinwen.html','r',encoding='utf-8')as f:
    html = f.read()
html = re.sub('{','|',html,flags=re.S)
html = re.sub('}','+',html,flags=re.S)
html = re.sub('\$','{',html,flags=re.S)
html = re.sub('\^','}',html,flags=re.S)
html = html.format(**message)
html = re.sub('\|','{',html,flags=re.S)
html = re.sub('\+','}',html,flags=re.S)
with open('测试.html','w',encoding='utf-8')as f:
    f.write(html)