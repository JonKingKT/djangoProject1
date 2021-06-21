from django.db import models

# Create your models here.
class Order(models.Model):
    id = models.CharField(max_length=20,primary_key=True,verbose_name='订单编号')
    create_time = models.CharField(max_length=20,verbose_name='订单创建时间')
    sell_id = models.CharField(max_length=10,verbose_name='卖家id')
    sell_name = models.CharField(max_length=100,verbose_name='卖家昵称')
    buy_id = models.CharField(max_length=10, verbose_name='买家id')
    buy_name = models.CharField(max_length=100,verbose_name='买家昵称')
    buy_phone = models.CharField(max_length=11,verbose_name='买家联系电话')
    address = models.CharField(max_length=200,verbose_name='买家地址')
    price = models.CharField(max_length=100,verbose_name='价格')
    goods_id = models.CharField(max_length=20, verbose_name='商品id')
    goods_name = models.CharField(max_length=100,verbose_name='物品名称')
    note = models.CharField(max_length=100,verbose_name='订单备注')
    state = models.CharField(max_length=10,verbose_name='订单状态')