#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/2/29 23:21
# @Author  : 亦轩
# @File    : urls.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index_views),
    url(r'login',views.index_views),
    url(r'logout',views.logout),
    url(r'detection/$',views.detection),
    url(r'upload/',views.upload),
    url(r'detection/doc/download', views.textdownload),
    url(r'fenjie/common/download',views.examining_report),
    url(r'file/package',views.file_package),
    url(r'retry', views.examining_report),
    url(r'detection/batchDownload',views.batchDownload),
    url(r'detectionlist/$',views.detectionlist),
    url(r'user/detection/list$',views.detectionlist),
    url(r'user/detection/doc/resubmit',views.resubmit),
    url(r'delete/data',views.deletedata),
    url(r'errorlist/',views.errorlist),
    url(r'docpack/add', views.adddocpack),
    url(r'docpack/',views.docpack),
    url(r'user/doc/delete',views.deletedoc),
    url(r'user/doc/list', views.docpack),
    url(r'order/',views.order),
    url(r'product/',views.product),
    url(r'user_info/',views.user_info),
    url(r'user_chpwd/',views.user_chpwd),
    ]
