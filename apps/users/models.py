from django.db import models

# Create your models here.
# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 用户信息
class UserProfile(AbstractUser):
    gender = models.CharField(max_length=6, choices=(("male", "男"),("female","女")), default="")
    birday = models.DateField(verbose_name="生日", null=True, blank=True)
    height = models.CharField(max_length=8, null=True, blank=True, verbose_name="身高")
    weight = models.CharField(max_length=8, null=True, blank=True, verbose_name="体重")
    city = models.CharField(max_length=8, null=True, blank=True, verbose_name="城市")
    spfamily = models.CharField(max_length=6, choices=(("1", "单亲家庭"), ("2", "非单亲")), default="2")
    education = models.CharField(max_length=6, null=True, blank=True, default="本科")
    one_child = models.CharField(max_length=6, choices=(("1", "独生子女"), ("2", "非独生子女")), default="1")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    mstatus = models.CharField(max_length=30, choices=(("never_married", "从未结婚"),
                                                        ("ivorce","离异"),("widowed","丧偶")), default="never_married")
    phone = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    wxNumber = models.CharField(max_length=20,null=True, blank=True, default="")
    work = models.CharField(max_length=6, null=True, blank=True, default="白领")
    salary = models.CharField(max_length=6, null=True, blank=True, default="10w")
    car = models.CharField(max_length=6, choices=(("1", "有车"),("2","没有")), default="2")
    home = models.CharField(max_length=6, choices=(("1", "有房"), ("2", "没有")), default="2")
    image = models.ImageField(upload_to="head/%Y/%m", verbose_name=u"headImg", max_length=100, default='')
    addtime = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# 手机验证码
class PhoneVerifyRecord(models.Model):
    CODE_CHOICES = (
        ('register', "注册"),
        ('forgetpw', "忘记密码")
    )
    code_type = models.CharField(null=True, blank=True, max_length=20, verbose_name="验证码类别",choices=CODE_CHOICES)
    phone = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    code = models.CharField(max_length=20, verbose_name=u"验证码", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = "手机验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.phone)