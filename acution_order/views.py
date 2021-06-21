import json

from django.shortcuts import render

# Create your views here.
import HttpReturn
from djangoProject1 import token
import djangoProject1.datautls
from acution_order import models as ao
from acution_user import models as au
from acution_goods import models as ag

# -1:购物车  1:已付款，待发货   2：收到货交易完成  3：已发货

def addGoodsToCart(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            user = au.acution_users.objects.filter(phone=user_phone).first()
            result = json.loads(request.body.decode()).get('nameValuePairs')
            id = result.get("id")
            name = result.get("name")
            price = result.get("price")
            sell_name = result.get("sell_name")
            info = result.get("info")
            category = result.get("category")
            create_time = str(djangoProject1.datautls.dateUtil())[0:20]
            goods_id = str(djangoProject1.datautls.dateUtil())[0:10]+str(ao.Order.objects.filter().count()+1)
            try:
                _user_account =ao.Order(id=goods_id,
                                            buy_id=user.id,
                                            buy_phone=user_phone,
                                            buy_name=user.name,
                                            address=user.address,
                                            goods_name=name,
                                            price=price,
                                            sell_name=sell_name,
                                            goods_id=id,
                                            create_time=create_time,
                                            state=str(-1)
                                            )
                _user_account.save()
                return HttpReturn.success(10000,'保存成功',1)
            except:
                return HttpReturn.success(10000,"保存失败",0)
        except:return HttpReturn.success(10000,'请求失败',-1)
    else:print("非post")


def ComfireOrder(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            user = au.acution_users.objects.filter(phone=user_phone).first()
            result = json.loads(request.body.decode()).get('nameValuePairs')
            id = result.get("id")
            name = result.get("name")
            price = result.get("price")
            sell_name = result.get("sell_name")
            info = result.get("info")
            category = result.get("category")
            order_id = result.get("order_id")
            create_time = str(djangoProject1.datautls.dateUtil())[0:20]
            user.balance-=float(price)
            # if(ag.acution_goods.objects.filter(name=name).count()>0):
            #     goods_id = ag.acution_goods.objects.filter(name=name).first().id
            # else:goods_id = str(djangoProject1.datautls.dateUtil())[0:18]+str(au.acution_users.objects.filter().count()+1)
            goods_id = str(djangoProject1.datautls.dateUtil())[0:10]+str(ao.Order.objects.filter().count()+1)
            if(order_id=='kong'):
                try:
                    _user_account =ao.Order(    id=goods_id,
                                                buy_id=user.id,
                                                buy_phone=user_phone,
                                                buy_name=user.name,
                                                address=user.address,
                                                goods_name=name,
                                                price=price,
                                                sell_name=sell_name,
                                                goods_id=id,
                                                note = info,
                                                create_time=create_time,
                                                state=str(1)
                                                )
                    _user_account.save()
                    user.save()
                    goods = ag.acution_goods.objects.get(id=id)
                    goods.create_time = 0
                    goods.save()
                    return HttpReturn.success(10000,'保存成功',user.balance)
                except:
                    return HttpReturn.success(10000,"保存失败",float(0))
            else:
                try:
                    orders = ao.Order.objects.get(id=order_id)
                    orders.state=0
                    orders.save()
                    return HttpReturn.success(10000, '保存成功', user.balance)
                except:return HttpReturn.success(10000,'请求失败',float(-1))
        except:return HttpReturn.success(10000,'请求失败',float(-1))
    else:print("非post")

def getShoppingCart(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            list=[]
            if (ao.Order.objects.filter(buy_phone=user_phone,state='-1').count() > 0):
                sreachresult = ao.Order.objects.filter(buy_phone=user_phone,state='-1')
                for i in sreachresult:
                    dict={}
                    dict['name'] = i.goods_name
                    dict['price'] = i.price
                    dict['info'] = ag.acution_goods.objects.filter(id=i.goods_id).first().info
                    dict['kind'] = ag.acution_goods.objects.filter(id=i.goods_id).first().kind
                    dict['sell_name']= i.sell_name
                    dict['goods_id'] = i.goods_id
                    dict['order_id'] = i.id
                    if(ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url is not None):
                        dict['goods_image_url'] = ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url
                    else:dict['goods_image_url']="kong"
                    list.append(dict)
                return HttpReturn.success(10000,'搜索商品信息成功',list)
            else:
                return HttpReturn.success(10000, '暂无此类商品', None)
        except:
            return HttpReturn.success(10000,"搜索失败",None)
    else:print("非post")


def delShoppingCart(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            result = json.loads(request.body.decode()).get('nameValuePairs')
            ao.Order.objects.get(id=result.get('order_id')).delete()
            return HttpReturn.success(10000,'删除成功',1)
        except:
            return HttpReturn.success(10000,"删除失败",0)
    else:print("非post")


def getReceiving(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            list=[]
            if ao.Order.objects.filter(buy_phone=user_phone, state='1').count() > 0:
                sreachresult = ao.Order.objects.filter(buy_phone=user_phone,state='1')
                for i in sreachresult:
                    dict={}
                    dict['name'] = i.goods_name
                    dict['price'] = i.price
                    dict['info'] = ag.acution_goods.objects.filter(id=i.goods_id).first().info
                    dict['kind'] = ag.acution_goods.objects.filter(id=i.goods_id).first().kind
                    dict['sell_name']= i.sell_name
                    dict['goods_id'] = i.goods_id
                    dict['order_id'] = i.id
                    dict['state'] =i.state
                    if(ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url is not None):
                        dict['goods_image_url'] = ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url
                    else:dict['goods_image_url']="kong"
                    list.append(dict)
            if ao.Order.objects.filter(buy_phone=user_phone, state='3').count() > 0:
                sreachresult = ao.Order.objects.filter(buy_phone=user_phone, state='3')
                for i in sreachresult:
                    dict = {}
                    dict['name'] = i.goods_name
                    dict['price'] = i.price
                    dict['info'] = ag.acution_goods.objects.filter(id=i.goods_id).first().info
                    dict['kind'] = ag.acution_goods.objects.filter(id=i.goods_id).first().kind
                    dict['sell_name'] = i.sell_name
                    dict['goods_id'] = i.goods_id
                    dict['order_id'] = i.id
                    dict['state'] = i.state
                    if (ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url is not None):
                        dict['goods_image_url'] = ag.acution_goods.objects.filter(
                            id=i.goods_id).first().goods_image_url
                    else:
                        dict['goods_image_url'] = "kong"
                    list.append(dict)
            return HttpReturn.success(10000,'搜索商品信息成功',list)
        except:
            return HttpReturn.success(10000,"搜索失败",None)
    else:print("非post")

def comfireReceiving(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            result = json.loads(request.body.decode()).get('nameValuePairs')
            order = ao.Order.objects.get(id=result.get('order_id'))
            order.state = 2
            sell_name = order.sell_name
            price = order.price
            order.save()
            user = au.acution_users.objects.get(name=sell_name)
            # user = au.acution_users.objects.filter(phone=user_phone).first()
            user.balance += float(price)
            user.save()
            return HttpReturn.success(10000,'收货成功',1)
        except:
            return HttpReturn.success(10000,"收货失败",0)
    else:print("非post")

def getReceived(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            list=[]
            if (ao.Order.objects.filter(buy_phone=user_phone,state='2').count() > 0):
                sreachresult = ao.Order.objects.filter(buy_phone=user_phone,state='2')
                for i in sreachresult:
                    dict={}
                    dict['name'] = i.goods_name
                    dict['price'] = i.price
                    dict['info'] = ag.acution_goods.objects.filter(id=i.goods_id).first().info
                    dict['kind'] = ag.acution_goods.objects.filter(id=i.goods_id).first().kind
                    dict['sell_name']= i.sell_name
                    dict['goods_id'] = i.goods_id
                    dict['order_id'] = i.id
                    if(ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url is not None):
                        dict['goods_image_url'] = ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url
                    else:dict['goods_image_url']="kong"
                    list.append(dict)
                return HttpReturn.success(10000,'搜索商品信息成功',list)
            else:
                return HttpReturn.success(10000, '暂无此类商品', None)
        except:
            return HttpReturn.success(10000,"搜索失败",None)
    else:print("非post")

def delReceived(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            result = json.loads(request.body.decode()).get('nameValuePairs')
            order = ao.Order.objects.get(id=result.get('order_id'))
            order.state = 100
            order.save()
            return HttpReturn.success(10000,'收货成功',1)
        except:
            return HttpReturn.success(10000,"收货失败",0)
    else:print("非post")

def getDispatched(request):
    if request.method == 'POST':
        try:
            _token = request.headers.get('token')
            # if _token is False:
            #     return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            list = []
            user = au.acution_users.objects.filter(phone=user_phone).first()
            if (ao.Order.objects.filter(buy_phone=user_phone, state='3').count() > 0):
                sreachresult = ao.Order.objects.filter(buy_phone=user_phone, state='3')
                for i in sreachresult:
                    dict = {}
                    dict['name'] = i.goods_name
                    dict['price'] = i.price
                    dict['info'] = ag.acution_goods.objects.filter(id=i.goods_id).first().info
                    dict['kind'] = ag.acution_goods.objects.filter(id=i.goods_id).first().kind
                    dict['sell_name'] = i.sell_name
                    dict['goods_id'] = i.goods_id
                    dict['order_id'] = i.id
                    if (ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url is not None):
                        dict['goods_image_url'] = ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url
                    else:
                        dict['goods_image_url'] = "kong"
                    list.append(dict)
                return HttpReturn.success(10000, '搜索商品信息成功', list)
            else:
                return HttpReturn.success(10000, '暂无此类商品', None)
        except:
            return HttpReturn.success(10000, "搜索失败", None)
    else:
        print("非post")

def delDispatched(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            result = json.loads(request.body.decode()).get('nameValuePairs')

            ag.acution_goods.objects.get(id=result.get('goods_id')).delete()

            return HttpReturn.success(10000,'删除成功',1)
        except:
            return HttpReturn.success(10000,"删除失败",0)
    else:print("非post")

def getSold(request):
    if request.method == 'POST':
        try:
            _token = request.headers.get('token')
            # if _token is False:
            #     return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            list = []
            user = au.acution_users.objects.filter(phone=user_phone).first()
            if (ao.Order.objects.filter(sell_name=user.name).count() > 0):
                sreachresult = ao.Order.objects.filter(sell_name=user.name)
                for i in sreachresult:
                    # if(ao.Order.objects.filter(goods_id=i.id).count()>0):
                    #     continue
                    dict = {}
                    dict['name'] = i.goods_name
                    dict['price'] = i.price
                    # dict['info'] = i.info
                    # dict['kind'] = i.kind
                    dict['sell_name'] = i.sell_id
                    dict['goods_id'] = i.goods_id
                    dict['order_id'] = i.id
                    dict['address'] = i.address
                    dict['note'] = i.note
                    dict['buy_phone'] = i.buy_phone
                    dict['buy_name'] = i.buy_name
                    dict['state'] = i.state
                    if (ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url is not None):
                        dict['goods_image_url'] = ag.acution_goods.objects.filter(id=i.goods_id).first().goods_image_url
                    else:
                        dict['goods_image_url'] = "kong"
                    list.append(dict)
                return HttpReturn.success(10000, '搜索商品信息成功', list)
            else:
                return HttpReturn.success(10000, '暂无此类商品', None)
        except:
            return HttpReturn.success(10000, "搜索失败", None)
    else:
        print("非post")

def comfireDispatch(request):
    if request.method =='POST':
        try:
            _token = request.headers.get('token')
            if _token is False:
                return HttpReturn.tokenOutTime()
            user_phone = token.get_userphone(_token)
            result = json.loads(request.body.decode()).get('nameValuePairs')
            order = ao.Order.objects.get(id=result.get('order_id'))
            order.state = '3'
            order.save()
            return HttpReturn.success(10000,'发货成功',1)
        except:
            return HttpReturn.success(10000,"发货失败",0)
    else:print("非post")

