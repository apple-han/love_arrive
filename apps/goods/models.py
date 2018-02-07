from django.db import models
from datetime import datetime

from DjangoUeditor.models import UEditorField
# Create your models here.

class Goods(models.Model):
    '''
    商品的信息
    '''
    category_id = models.IntegerField(default=0, verbose_name="三级分类")
    second_id = models.IntegerField(default=0, verbose_name="二级分类")
    first_id = models.IntegerField(default=0, verbose_name="一级分类")
    goods_sn = models.CharField(verbose_name="商品唯一的货号", max_length=50, default="",null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name="商品名",default='',null=True, blank=True)
    url = models.CharField(max_length=500, verbose_name="商品连接",default='',null=True, blank=True)
    brand = models.CharField(max_length=100, verbose_name="商品品牌", default='',null=True, blank=True)
    click_num = models.IntegerField(default=0, verbose_name="点击数",blank=True)
    sold_num = models.IntegerField(default=0, verbose_name="商品的销售量",blank=True)
    fav_num = models.IntegerField(default=0, verbose_name="收藏数",null=True, blank=True)
    goods_num = models.IntegerField(default=0, verbose_name="库存数",null=True, blank=True)
    price = models.FloatField(default=0, verbose_name="本店价格",null=True, blank=True)
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述",null=True, blank=True)
    goods_desc = UEditorField(verbose_name=u"内容", imagePath="goods/images/", width=1000, height=300,
                              filePath="goods/files/", default='')
    pic = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", null=True, blank=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords

class GetIp(models.Model):
    '''
    ip地址库
    '''
    ip = models.CharField(default="", max_length=80, verbose_name="ip地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")