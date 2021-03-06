# Generated by Django 3.2.4 on 2021-06-14 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='acution_goods',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='商品id')),
                ('sell_id', models.CharField(max_length=10, verbose_name='卖家ID')),
                ('name', models.CharField(max_length=100, verbose_name='商品名称')),
                ('create_time', models.CharField(max_length=40, verbose_name='商品上传时间')),
                ('info', models.CharField(max_length=100, verbose_name='商品简介')),
                ('kind', models.CharField(max_length=50, verbose_name='商品品类')),
                ('goods_image', models.FileField(upload_to='goods_image', verbose_name='商品图片')),
                ('price', models.CharField(max_length=10, verbose_name='商品价格')),
                ('goods_image_url', models.CharField(max_length=100, verbose_name='商品图片路径')),
            ],
        ),
    ]
