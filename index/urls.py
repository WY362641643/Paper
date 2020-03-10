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
    ]