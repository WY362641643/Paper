#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/10 18:46
# @Author  : 亦轩
# @File    : urls.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
from django.conf.urls import url
from index import views
urlpatterns = [
    url(r'^$', views.index_views),
    url(r'^/submit',views.cnki),
    url('^/upload_file',views.upload_file),
    url('/ajax_check_order',views.ajax_check_order),
    url('^/multiple$',views.multiple),
    url('^/multiple/upload_file$',views.multiple_upload_file),
    url('^/multiple/submit$',views.multiple),
    url('/report/tid/(?P<order>\s{12,32}|\d{12,32})$',views.report_tid_order),
    url('^/report$',views.report),
    url('^/ajax_search_order',views.ajax_search_order),
    url('^/get_site_info_common',views.ajax_search_order),
    url('^/report/tid/(?P<order>\s{12,32}|\d{12,32})/sid/(?P<id>\d+)',views.download),
    url('^/ajax_del_report',views.ajax_del_report),
    ]