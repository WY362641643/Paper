from django.db import models

# Create your models here.

class Users(models.Model):
    account = models.CharField(max_length=12,unique=True,verbose_name='账户')
    password = models.CharField(max_length=12,verbose_name='密码')
    vx = models.CharField(max_length=16,null=True,blank=True,verbose_name='微信号')
    phone = models.CharField(max_length=12,null=True,blank=True,verbose_name='电话')
    qq = models.CharField(max_length=16,null=True,blank=True,verbose_name='QQ号')
    website = models.CharField(max_length=64,null=True,blank=True,verbose_name='网站')
    domain = models.CharField(max_length=64,null=True,blank=True,verbose_name='域名')

    # 重写__str__函数3
    def __str__(self):
        return self.account

    class Meta:
        db_table = "users"
        verbose_name = '代理列表'
        verbose_name_plural = verbose_name

    def dic(self):
        d ={
            'account':self.account,
            'password':self.password,
            'vx':self.vx,
            'phone':self.phone,
            'qq':self.qq,
            'website':self.website,
            'domain':self.domain,
        }
        return d
# 绑定用户各种检测次数
class Surplus(models.Model):
    account = models.ForeignKey(Users,on_delete=models.CASCADE,verbose_name='用户')
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
            'A':self.a,
            'P':self.p,
            'V':self.v
        }
        return d
# 检测卡列表
class IsActivateCode(models.Model):
    card = models.CharField(max_length=12,unique=True,verbose_name='卡号')
    isActivate = models.BooleanField(default=True,verbose_name='是否销毁')

    # 重写__str__函数3
    def __str__(self):
        return str(self.card)

    class Meta:
        db_table = "isactivatecode"
        verbose_name = '检测卡'
        verbose_name_plural = verbose_name
# 检测列表
class DetectionList(models.Model):
    account = models.ForeignKey(Users,on_delete=models.CASCADE,verbose_name='用户')
    orderacc = models.CharField(max_length=16,null=True,blank=True,verbose_name='订单编号')
    title = models.CharField(max_length=64,null=True,blank=True,verbose_name='标题')
    author = models.CharField(max_length=16,null=True,blank=True,verbose_name='作者')
    date = models.CharField(max_length=14,null=True,blank=True,verbose_name='提交时间')
    iscode = models.IntegerField(null=True,blank=True,default=-2,verbose_name='状态')
        # --状态 -2文件解析出错 ,-1待提交： 0待检测， 1检测中， 2等待获取报告, 3正在生产报告, 4检测完成
    similarity = models.FloatField(null=True,blank=True,default=0,verbose_name='相似度') # --相似度，值区间0~1
    taskid = models.CharField(max_length=38,blank=True,verbose_name='taskid')
    filepath = models.CharField(max_length=254,default='',verbose_name='文本路径')
    zipurl = models.URLField(blank=True,null=True,verbose_name='报告压缩包地址')

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "detectionlist"
        verbose_name = '检测列表'
        verbose_name_plural = verbose_name
    def dic(self):
        d = {
            'id':self.id,
            'orderid':self.orderacc,
            'title':self.title,
            'author':self.author,
            'postTime':self.date,
            'state':self.iscode,
            'similarity':self.similarity,
            'taskid':self.taskid,
            'zipurl':self.zipurl,
        }
        return d
# 错误列表
class ErrotList(models.Model):
    account = models.ForeignKey(Users,on_delete=models.CASCADE,verbose_name='用户')
    orderacc = models.CharField(max_length=16,null=True,blank=True,verbose_name='订单编号')
    title = models.CharField(max_length=64,null=True,blank=True,verbose_name='标题')
    author = models.CharField(max_length=16,null=True,blank=True,verbose_name='作者')
    date = models.CharField(max_length=14,null=True,blank=True,verbose_name='提交时间')

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "errorlist"
        verbose_name = '错误列表'
        verbose_name_plural = verbose_name
# 打包文档
class order(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户')
    orderacc = models.CharField(max_length=20,null=True,blank=True,verbose_name='订单号')
    date = models.CharField(max_length=14, null=True, blank=True, verbose_name='时间')
    number = models.IntegerField(null=True,blank=True,verbose_name='可用件数')
    operation = models.CharField(null=True,blank=True,max_length=8,verbose_name='操作')

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "order"
        verbose_name = '订单管理列表'
        verbose_name_plural = verbose_name
# 订单管理
class Treasure(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户')
    website = models.CharField(max_length=128,null=True,blank=True,verbose_name='域名')
    individuation = models.CharField(max_length=32,null=True,blank=True,verbose_name='个性化')
    treid = models.CharField(max_length=16,null=True,blank=True,verbose_name='宝贝ID')
    WW = models.CharField(max_length=16,null=True,blank=True,verbose_name='旺旺')
    qq = models.CharField(max_length=16,null=True,blank=True,verbose_name='QQ')
    phone = models.CharField(max_length=12,null=True,blank=True,verbose_name='电话')
    iscode = models.BooleanField(default=True,blank=True,verbose_name='授权状态')
    date = models.CharField(max_length=14,null=True,blank=True,verbose_name='授权时间')
    operation = models.CharField(max_length=12,null=True,blank=True,verbose_name='操作')

    # 重写__str__函数3
    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = "treasure"
        verbose_name = '宝贝管理'
        verbose_name_plural = verbose_name

class Globo(models.Model):
    name = models.CharField(max_length=8,verbose_name='名称')
    info = models.CharField(max_length=128,verbose_name='信息')

    # 重写__str__函数3
    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "globo"
        verbose_name = '全局管理'
        verbose_name_plural = verbose_name