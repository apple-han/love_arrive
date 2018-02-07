# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class UserImage(models.Model):
    """
    用户头像表
    """
    user = models.ForeignKey(User, verbose_name="用户",default='')
    file = models.FileField(upload_to="message/images/", verbose_name="上传的照片", help_text="上传的文件")
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户照片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
#
class UserConcernlove(models.Model):
    """
    用户关注表
    """
    userConcern = models.ForeignKey(User, verbose_name="关注人", default='')
    concertuser = models.ForeignKey(User, related_name='被关注人',verbose_name="被关注人", default='')
    matchsucess = models.CharField(max_length=6, choices=(("0", "匹配成功"), ("1", "单相思")), default="1")
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户关注"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userConcern.username
