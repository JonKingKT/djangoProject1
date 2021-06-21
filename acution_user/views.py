import json

from django.shortcuts import render

# Create your views here.

import HttpReturn
import djangoProject1.datautls
from djangoProject1 import token
from acution_user import models


def register(request):
    if request.method =='POST':
        try:
            a = request.body.decode()
            result1 = json.loads(a)
            result = result1.get('nameValuePairs')
            user_phone =result.get('userphone',None)
            user_password = result.get('userpassword',None)
            user_name = result.get('username',None)
            user_address = result.get('useraddress',None)
            user_balance = 0
            user_createtime = djangoProject1.datautls.dateUtil()
            user_id =  str(djangoProject1.datautls.dateUtil())[0:7]
            user_id = user_id+ str(models.acution_users.objects.filter().count()+1)
            if models.acution_users.objects.filter(phone=user_phone).count()>0:
                return HttpReturn.success(10000,"用户已存在",2)
            else:
                try:
                    _user_account =models.acution_users(phone=user_phone,
                                                      password=user_password,
                                                      name=user_name,
                                                      balance=user_balance,
                                                      create_time=user_createtime,
                                                      address=user_address,
                                                      id=user_id)
                    _user_account.save()
                    return HttpReturn.success(10000,'注册成功',1)
                except:
                    return HttpReturn.success(10000,"注册失败",0)
        except:return HttpReturn.success(0,'请求失败',0)
    else:print("非post")

def judge_phone(request):
    if request.method =='POST':
        try:
            a = request.body.decode()
            result = json.loads(a)
            user_phone =result.get('userphone',None)

            if models.acution_users.objects.filter(phone=user_phone).count()>0:
                return HttpReturn.success(10000,"用户已存在",0)
            else:
                try:

                    return HttpReturn.success(10000,'请求成功',1)
                except:
                    return HttpReturn.success(10000,"注册失败",0)
        except:return HttpReturn.success(0,'请求失败',0)
    else:print("非post")

def login(request):
    try:
        result = json.loads(request.body.decode()).get('nameValuePairs')
        user_phone = result.get('user_phone',None)
        user_password = result.get('user_password',None)
        if models.acution_users.objects.filter(phone=user_phone).count()==0:
            return HttpReturn.success(10000,'用户不存在',"0")
        else:
            user = models.acution_users.objects.filter(phone=user_phone).first()
            if user_password != user.password:
                return  HttpReturn.success(10000,'密码错误',"1")
            else:return HttpReturn.success(10000,'登陆成功', token.create_user_token(user_phone))
    except:return HttpReturn.success(10000,'登陆失败',"-1")

def getUserInfo(request):
    try:
        _token = request.headers.get('token')
        if token.check_user_token(_token) is False:
            return  HttpReturn.tokenOutTime()
        user_phone = token.get_userphone(_token)
        user = models.acution_users.objects.filter(phone=user_phone).first()

        return HttpReturn.success(10000,'获取成功',data={
            'callphone':user_phone,'name':user.name,
            'address':user.address,'id':user.id,'blance':user.balance})
    except:return HttpReturn.success(10000,'获取失败',0)


def reCharge(request):
    try:
        _token = request.headers.get('token')
        # if token.check_user_token(_token) is False:
        #     return  HttpReturn.tokenOutTime()
        user_phone = token.get_userphone(_token)
        user = models.acution_users.objects.get(phone=user_phone)
        result = json.loads(request.body.decode()).get('nameValuePairs')
        user.balance += result.get('balance')
        print(user.balance)
        user.save()
        return HttpReturn.success(10000,'获取成功',user.balance)
    except:return HttpReturn.success(10000,'获取失败',float(0))

def editUserInfo(request):
    try:
        _token = request.headers.get('token')
        user_phone = token.get_userphone(_token)
        result = json.loads(request.body.decode()).get('nameValuePairs')
        user_password = result.get('user_password')
        user_name = result.get('user_name')
        user_address = result.get('user_address')
        user = models.acution_users.objects.get(user_phone=user_phone)
        if user_password is not None:
            user.password = user_password
        if user_name is not  None:
            user.name = user_name
        if user_address is not None:
            user.address = user_address
        user.save()
        HttpReturn.success(10000,'修改成功',1)
    except:return HttpReturn.success(10000,'登陆失败',0)