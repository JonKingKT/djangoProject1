from django.db import models
from django.contrib import admin


# Create your models here.

class acution_users(models.Model):
    id = models.CharField(primary_key=True, verbose_name='用户id', max_length=10)
    name = models.CharField(max_length=20, verbose_name='用户名字')
    phone = models.CharField(max_length=11, verbose_name='用户手机号')
    info = models.CharField(max_length=100, verbose_name='用户简介')
    password = models.CharField(max_length=16, verbose_name='用户登录密码')
    address = models.CharField(max_length=140,verbose_name='用户收货地址')
    create_time = models.CharField(max_length=40,verbose_name='用户创建时间')
    user_image = models.ImageField(upload_to='userface',default='ic_defultuserface.png')
    balance =models.FloatField(max_length=10,verbose_name='用户余额')


class acution_user_admin(admin.ModelAdmin):
    list_display = ('id','name')