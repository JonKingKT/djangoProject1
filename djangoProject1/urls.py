"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import acution_goods.views
import acution_order.views
import acution_user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',acution_user.views.register),
    path('login/',acution_user.views.login),
    path('getuserInfo/',acution_user.views.getUserInfo),
    path('addGoods/',acution_goods.views.addGoods),
    path('addGoodsPic/',acution_goods.views.addGoodsPic),
    path('addGoodsToCart/',acution_order.views.addGoodsToCart),
    path('comfireOrder/',acution_order.views.ComfireOrder),
    path('getSreachResult/',acution_goods.views.getGoodsSreachInfo),
    path('getShoppingCart/',acution_order.views.getShoppingCart),
    path('delShopCart/',acution_order.views.delShoppingCart),
    path('balanceRecharge/',acution_user.views.reCharge),
    path('getReceiving/',acution_order.views.getReceiving),
    path('comfireReceiving/',acution_order.views.comfireReceiving),
    path('getReceived/',acution_order.views.getReceived),
    path('delReceived/',acution_order.views.delReceived),
    path('getDispatched/',acution_order.views.getDispatched),
    path('delDispatched/',acution_order.views.delDispatched),
    path('getSold/',acution_order.views.getSold),
    path('comfireDispatch/',acution_order.views.comfireDispatch),
    path('getAllGoods/',acution_goods.views.getAllGoods),
    path('editUserInfo/',acution_user.views.editUserInfo),
]
