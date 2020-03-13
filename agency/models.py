from django.db import models
import time

# Create your models here.

class Users(models.Model):
    account = models.CharField(max_length=12, unique=True, verbose_name='账户')
    password = models.CharField(max_length=12, verbose_name='密码')
    vx = models.CharField(max_length=16, null=True, blank=True, verbose_name='微信号')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='电话')
    qq = models.CharField(max_length=16, null=True, blank=True, verbose_name='QQ号')
    website = models.CharField(max_length=64, null=True, blank=True, verbose_name='网站')
    domain = models.CharField(max_length=64, null=True, blank=True, verbose_name='域名')

    # 重写__str__函数3
    def __str__(self):
        return self.account

    class Meta:
        db_table = "users"
        verbose_name = '代理列表'
        verbose_name_plural = verbose_name

    def dic(self):
        d = {
            'account': self.account,
            'password': self.password,
            'vx': self.vx,
            'phone': self.phone,
            'qq': self.qq,
            'website': self.website,
            'domain': self.domain,
        }
        return d
# 绑定代理商各种检测次数
class Surplus(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='代理商')
    a = models.IntegerField(default=0, blank=True, verbose_name='A剩余')
    p = models.IntegerField(default=0, blank=True, verbose_name='P剩余')
    v = models.IntegerField(default=0, blank=True, verbose_name='V剩余')

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "surplus"
        verbose_name = '代理充值'
        verbose_name_plural = verbose_name

    def dic(self):
        d = {
            'A': self.a,
            'P': self.p,
            'V': self.v,
        }
        return d
# 检测卡列表
class IsActivateCode(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='代理商')
    card = models.CharField(max_length=12, unique=True, verbose_name='卡号')
    isActivate = models.BooleanField(default=False, verbose_name='是否已使用')

    # 重写__str__函数3
    def __str__(self):
        return str(self.card)

    class Meta:
        db_table = "isactivatecode"
        verbose_name = '检测卡'
        verbose_name_plural = verbose_name
num = {
    -2: '0',
    1: '0',
    4: '1',
    5:'2'
}
strs = {
    -2: '正在检测中',
    1: '正在检测中',
    4: '完成',
    5:'完成',
}

#将当前时间转换为时间字符串，默认为2017-10-01 13:37:04格式
def now_to_date(times,format_string="%Y-%m-%d %H:%M:%S"):
 time_stamp = int(int(times)/1000)
 time_array = time.localtime(time_stamp)
 str_date = time.strftime(format_string, time_array)
 return str_date
# 检测列表
class DetectionList(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='代理商')
    orderacc = models.CharField(max_length=19, null=True, blank=True, verbose_name='订单编号')
    title = models.CharField(max_length=64, null=True, blank=True, verbose_name='标题')
    author = models.CharField(max_length=16, null=True, blank=True, verbose_name='作者')
    date = models.CharField(max_length=20, null=True, blank=True, verbose_name='提交时间')
    report_date = models.CharField(max_length=20,null=True,blank=True,default='',verbose_name='完成时间')
    iscode = models.IntegerField(null=True, blank=True, default=-2, verbose_name='状态')
    # --状态 -2文件解析出错 ,-1待提交： 0待检测， 1检测中， 2等待获取报告, 3正在生产报告, 4检测完成
    similarity = models.FloatField(null=True, blank=True, default=0, verbose_name='相似度')  # --相似度，值区间0~1
    textnumber = models.IntegerField(default=0, verbose_name='文章字符数')
    taskid = models.CharField(max_length=38, blank=True, verbose_name='taskid')
    filepath = models.CharField(max_length=254, default='', verbose_name='文本路径')
    zipurl = models.URLField(blank=True, null=True, verbose_name='报告压缩包地址')
    isclear = models.BooleanField(default=False,verbose_name='用户是否删除')

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "detectionlist"
        verbose_name = '检测列表'
        verbose_name_plural = verbose_name

    def dic(self):
        d = {
            'id': self.id,
            'orderid': self.orderacc,
            'title': self.title,
            'author': self.author,
            'postTime': self.date,
            'state': self.iscode,
            'similarity': self.similarity,
            'taskid': self.taskid,
            'zipurl': self.zipurl,
            'matchNo': self.textnumber,
        }
        return d

    def dicreport(self):
        d = {"tid": self.orderacc,
             "sid": self.id,
             "chk_type": "3",
             "type": "VIP\/TMLC2",
             "title": self.title,
             "author": self.author,
             "add_date": now_to_date(self.date),
             "report_date": self.report_date,
             "wordnum": "3253",
             "price": "1.00",
             "report_day": 0,
             "reduce_guide": 0,
             "status": {"num": num[self.iscode],
                        "str": strs[self.iscode],
                        "color": "black",
                        "extra": "报告已删除",
                        "is_change_paper": 0,
                        "is_report_expire": 0},
             "query_time": self.date,
             "check_url": "http://www.cnkidata.com/"}
        return d
# 错误列表
class ErrotList(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='代理商')
    orderacc = models.CharField(max_length=16, null=True, blank=True, verbose_name='订单编号')
    title = models.CharField(max_length=64, null=True, blank=True, verbose_name='标题')
    author = models.CharField(max_length=16, null=True, blank=True, verbose_name='作者')
    date = models.CharField(max_length=20, null=True, blank=True, verbose_name='提交时间')

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "errorlist"
        verbose_name = '错误列表'
        verbose_name_plural = verbose_name
# 打包文档
class Packdocument(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='代理商')
    filename = models.CharField(null=True, blank=True, max_length=128, verbose_name='文档名称')

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "packdocument"
        verbose_name = '打包文档'
        verbose_name_plural = verbose_name

    def dic(self):
        d = {
            'id': self.id,
            'filename': self.filename,
        }
        return d
# 订单管理
class Order(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='代理商')
    types = models.CharField(max_length=4, default='A', verbose_name='订单类型')
    ordernumber = models.CharField(max_length=20,unique=True, default=0, verbose_name='订单号')
    date = models.CharField(max_length=20, default=0, verbose_name='时间')
    quantity_residual = models.IntegerField(default=0, verbose_name='剩余数量')
    payment = models.CharField(max_length=16, verbose_name='实付金额')
    freeze = models.BooleanField(default=False,verbose_name='是否冻结')
    # 重写__str__函数3
    def __str__(self):
        return str(self.account)
    class Meta:
        db_table = "order"
        verbose_name = '订单管理列表'
        verbose_name_plural = verbose_name

    def dic(self):
        d = {
            'orderid':self.ordernumber,
            'addTime':self.date,
            'num':self.quantity_residual,
        }
        return d
# 宝贝管理
class Treasure(models.Model):
    GENDER = (
        ('A', 'A类型,5W字以内'),
        ('P', 'P类型,15W字以内'),
        ('V', 'V类型,25W字以内'),
    )
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='代理商')
    website = models.CharField(max_length=128, null=True, blank=True, verbose_name='域名')
    individuation = models.CharField(max_length=32, null=True, blank=True, verbose_name='个性化')
    treid = models.CharField(max_length=16, null=True, unique=True, blank=True, verbose_name='宝贝ID')
    WW = models.CharField(max_length=16, null=True, blank=True, verbose_name='旺旺')
    qq = models.CharField(max_length=16, null=True, blank=True, verbose_name='QQ')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='电话')
    iscode = models.BooleanField(default=True, blank=True, verbose_name='授权状态')
    date = models.CharField(max_length=20, null=True, blank=True, verbose_name='授权时间')
    operation = models.CharField(max_length=12, null=True, blank=True, verbose_name='操作')
    xitong = models.CharField(choices=GENDER, max_length=6, verbose_name="类型")

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "treasure"
        verbose_name = '宝贝管理'
        verbose_name_plural = verbose_name

    def dic(self):
        d = {
            'id':self.id,
            'serverName':'http://www.cnkidata.com',
            'domain':self.xitong,
            'productid':self.treid,
            'wangwang':self.WW,
            'qq':self.qq,
            'phone':self.phone,
            'authorized':self.iscode,
            'lastAuthTime':self.date,
            'xitong':self.xitong,
            'authorizedUrl':'http://alds.agiso.com/Authorize.aspx?appId=20190520341920&state=2233',
        }
        return d
# 全局管理
class Globo(models.Model):
    name = models.CharField(max_length=8, verbose_name='名称')
    info = models.CharField(max_length=128, verbose_name='信息')
    isActivate = models.BooleanField(default=True, verbose_name='是否激活')

    # 重写__str__函数3
    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "globo"
        verbose_name = '全局管理'
        verbose_name_plural = verbose_name
