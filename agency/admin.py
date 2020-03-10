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
class DetectionListAdmin(admin.ModelAdmin):
    list_display = ('account','orderacc','title','author','date','iscode','similarity','textnumber','taskid','filepath','zipurl')  # 显示的字段
    list_display_links = ('account',)  # 链接的字段
    list_editable = ('title','author','date','iscode','similarity','textnumber','taskid','filepath','zipurl')  # 在列表页中可修改的字段
    list_fields = ('orderacc','date','textnumber')  # 在列表页的右侧增加过滤器实现快速筛选
    search_fields = ('orderacc','title','author')  # 添加搜索字段
    # fields = ('name','email') # 在详情页中,指定要显示的字段以及顺序
    list_filter = ('date','textnumber') # 在列表页的右侧增加过滤器实现快速筛选
    # ordering = ('-downloads',)
    # date_hierarchy = 'register'  # 指定时间分成选择器
class PackdocumentAdmin(admin.ModelAdmin):
    list_display = ('account','filename')  # 显示的字段
    list_display_links = ('account',)  # 链接的字段
    list_editable = ('filename',)  # 在列表页中可修改的字段
    list_fields = ('filename',)  # 在列表页的右侧增加过滤器实现快速筛选
    search_fields = ('filename',)  # 添加搜索字段
    # fields = ('name','email') # 在详情页中,指定要显示的字段以及顺序
    # list_filter = ('date','textnumber') # 在列表页的右侧增加过滤器实现快速筛选
    # ordering = ('-downloads',)
    # date_hierarchy = 'register'  # 指定时间分成选择器
class OrderAdmin(admin.ModelAdmin):
    list_display = ('account','ordernumber','date','quantity_residual')  # 显示的字段
    list_display_links = ('account',)  # 链接的字段
    list_editable = ('ordernumber','date','quantity_residual')  # 在列表页中可修改的字段
    list_fields = ('date','quantity_residual')  # 在列表页的右侧增加过滤器实现快速筛选
    search_fields = ('date','quantity_residual')  # 添加搜索字段
    # fields = ('name','email') # 在详情页中,指定要显示的字段以及顺序
    list_filter = ('date','quantity_residual') # 在列表页的右侧增加过滤器实现快速筛选
    # ordering = ('-downloads',)
    # date_hierarchy = 'register'  # 指定时间分成选择器
class TreasureAdmin(admin.ModelAdmin):
    list_display = ('account','website', 'individuation', 'treid', 'WW', 'qq', 'phone', 'iscode', 'date',)  # 显示的字段
    list_display_links = ('account',)  # 链接的字段
    list_editable = ('website', 'individuation', 'treid', 'WW', 'qq', 'phone', 'iscode', 'date',)  # 在列表页中可修改的字段
    list_fields = ('website', 'individuation', 'treid', 'WW', 'qq', 'phone', 'iscode', 'date',)  # 在列表页的右侧增加过滤器实现快速筛选
    search_fields = ('website', 'individuation', 'treid', 'WW', 'qq', 'phone', 'iscode', 'date',)  # 添加搜索字段
    # fields = ('name','email') # 在详情页中,指定要显示的字段以及顺序
    list_filter = ('website', 'individuation', 'treid', 'WW', 'qq', 'phone', 'iscode', 'date',) # 在列表页的右侧增加过滤器实现快速筛选
    # ordering = ('-downloads',)
    # date_hierarchy = 'register'  # 指定时间分成选择器
class GloboAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'isActivate',)  # 显示的字段
    list_display_links = ('name',)  # 链接的字段
    list_editable = ( 'info', 'isActivate',)  # 在列表页中可修改的字段
    list_fields = ( 'info', 'isActivate',)  # 在列表页的右侧增加过滤器实现快速筛选
    search_fields = ( 'info', 'isActivate',)  # 添加搜索字段
    # fields = ('name','email') # 在详情页中,指定要显示的字段以及顺序
    list_filter = ( 'info', 'isActivate',) # 在列表页的右侧增加过滤器实现快速筛选
    # ordering = ('-downloads',)
    # date_hierarchy = 'register'  # 指定时间分成选择器
admin.site.register(Users,UsersAdmin)
admin.site.register(Surplus,SurplusAdmin)
admin.site.register(IsActivateCode,IsActivateCodeAdmin)
admin.site.register(DetectionList,DetectionListAdmin)
admin.site.register(Packdocument,PackdocumentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Treasure,TreasureAdmin)
admin.site.register(Globo,GloboAdmin)
