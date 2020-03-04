from django.contrib import admin
from .models import *
# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = ('account','password','vx','phone','qq','website','domain')  # 显示的字段
    list_display_links = ('account',)  # 链接的字段
    list_editable = ('password','vx','phone','qq','website','domain')  # 在列表页中可修改的字段
    # list_fields = ('downloads',)  # 在列表页的右侧增加过滤器实现快速筛选
    # search_fields = ('name',)  # 添加搜索字段
    # fields = ('name','email') # 在详情页中,指定要显示的字段以及顺序
    # list_filter = ('isActivate',) # 在列表页的右侧增加过滤器实现快速筛选
    # ordering = ('-downloads',)
    # date_hierarchy = 'register'  # 指定时间分成选择器

class SurplusAdmin(admin.ModelAdmin):
    list_display = ('account','a','p','v')  # 显示的字段
    list_display_links = ('account',)  # 链接的字段
    list_editable = ('a','p','v')  # 在列表页中可修改的字段
    # list_fields = ('downloads',)  # 在列表页的右侧增加过滤器实现快速筛选
    # search_fields = ('name',)  # 添加搜索字段
    # fields = ('name','email') # 在详情页中,指定要显示的字段以及顺序
    # list_filter = ('isActivate',) # 在列表页的右侧增加过滤器实现快速筛选
    # ordering = ('-downloads',)
    # date_hierarchy = 'register'  # 指定时间分成选择器
class IsActivateCodeAdmin(admin.ModelAdmin):
    list_display = ('card','isActivate')  # 显示的字段
    list_display_links = ('card',)  # 链接的字段
    # list_editable = ('a','p','v')  # 在列表页中可修改的字段
    # list_fields = ('downloads',)  # 在列表页的右侧增加过滤器实现快速筛选
    # search_fields = ('name',)  # 添加搜索字段
    # fields = ('name','email') # 在详情页中,指定要显示的字段以及顺序
    # list_filter = ('isActivate',) # 在列表页的右侧增加过滤器实现快速筛选
    # ordering = ('-downloads',)
    # date_hierarchy = 'register'  # 指定时间分成选择器

admin.site.register(Users,UsersAdmin)
admin.site.register(Surplus,SurplusAdmin)
admin.site.register(IsActivateCode,IsActivateCodeAdmin)