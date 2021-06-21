import json

import HttpReturn
import djangoProject1.datautls
from django.shortcuts import render
# Create your views here.
from djangoProject1 import token
from acution_order import models as ao
from acution_user import models as au
from acution_goods import models as ag


def addGoods(request):
    if request.method =='POST':
        # try:
        _token = request.headers.get('token')
        if _token is False:
            return HttpReturn.tokenOutTime()
        user_phone = token.get_userphone(_token)
        result = json.loads(request.body.decode()).get('nameValuePairs')
        id = result.get("id")
        name = result.get("name")
        price = result.get("price")
        sell_name = result.get("sell_name")
        info = result.get("info")
        category = result.get("category")
        pic_url = result.get("pic_url")
        # create_time = str(djangoProject1.datautls.dateUtil())
        if(id=='kong'):
            id = str(djangoProject1.datautls.dateUtil())[0:10]+str(ag.acution_goods.objects.filter().count()+1)
        if(sell_name==None):
            sell_name = au.acution_users.objects.filter(phone=user_phone).first().name
        # try:
        _user_account =ag.acution_goods(id=id,
                                            name=name,
                                            price=price,
                                            sell_id=sell_name[0:9],
                                            info=info,
                                            kind=category,
                                            create_time=1,
                                            goods_image_url=pic_url)
        _user_account.save()
        return HttpReturn.success(10000,'保存成功',1)
        #     except:
        #         return HttpReturn.success(10000,"保存失败",0)
        # except:return HttpReturn.success(10000,'请求失败',0)
    else:print("非post")


def addGoodsPic(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()

            try:
                _user_account =ag.acution_goods(id=123)
                _user_account.save()
                return HttpReturn.success(10000,'注册成功',1)
            except:
                return HttpReturn.success(10000,"注册失败",0)
        except:return HttpReturn.success(0,'请求失败',0)
    else:print("非post")


def getGoodsSreachInfo(request):
    if request.method =='POST':
        try:
            result = json.loads(request.body.decode()).get('nameValuePairs')
            list=[]
            if (ag.acution_goods.objects.filter(name__contains=result.get("sreach")).count() > 0):
                sreachresult = ag.acution_goods.objects.filter(name__contains=result.get("sreach"))
                for i in sreachresult:
                    dict={}
                    dict['name'] = i.name
                    dict['price'] = i.price
                    dict['info'] = i.info
                    dict['kind'] = i.kind
                    dict['sell_name']= i.sell_id
                    dict['goods_id'] = i.id
                    if(i.goods_image_url is not None):
                        dict['goods_image_url'] = i.goods_image_url
                    else:dict['goods_image_url']="kong"
                    list.append(dict)
                return HttpReturn.success(10000,'搜索商品信息成功',list)
            else:
                return HttpReturn.success(10000, '暂无此类商品', None)
        except:
            return HttpReturn.success(10000,"搜索失败",None)
    else:print("非post")

def getAllGoods(request):
    if request.method =='POST':
        try:
            list=[]
            sreachresult = ag.acution_goods.objects.filter(create_time=1)
            for i in sreachresult:
                dict={}
                dict['name'] = i.name
                dict['price'] = i.price
                dict['info'] = i.info
                dict['kind'] = i.kind
                dict['sell_name']= i.sell_id
                dict['goods_id'] = i.id
                if(i.goods_image_url is not None):
                    dict['goods_image_url'] = i.goods_image_url
                else:dict['goods_image_url']="kong"
                list.append(dict)
            return HttpReturn.success(10000,'搜索商品信息成功',list)
        except:
            return HttpReturn.success(10000,"搜索失败",None)
    else:print("非post")


