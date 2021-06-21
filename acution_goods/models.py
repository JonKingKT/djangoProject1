from django.db import models
from django.contrib import admin

# Create your models here.
class acution_goods(models.Model):
    id = models.CharField(primary_key=True, verbose_name='商品id', max_length=20)
    sell_id = models.CharField(max_length=10,verbose_name="卖家ID")
    name = models.CharField(max_length=100, verbose_name='商品名称')
    create_time = models.CharField(max_length=40,verbose_name='商品上传时间')
    info = models.CharField(max_length=100, verbose_name='商品简介')
    kind = models.CharField(max_length=50,verbose_name='商品品类')
    goods_image = models.FileField(upload_to='goods_image',verbose_name='商品图片')
    price = models.CharField(max_length=10,verbose_name='商品价格')
    goods_image_url = models.CharField(max_length=100,verbose_name='商品图片路径')


class acution_goods_register(admin.ModelAdmin):
    list_display = ('id','name')