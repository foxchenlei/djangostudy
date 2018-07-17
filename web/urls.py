#coding=utf-8
"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from ops import views as v

#from kvm import urls as kvm.urls
import kvm


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', v.index),
    url(r'^login/', v.login),
    url(r'^register/', v.register),
    url(r'^logout', v.logout),
    url(r'^captcha', include('captcha.urls')),
    url(r'^confirm/$', v.user_confirm),

    url(r'^assets/', include('cmdb.urls')),


    url(r'^simplemap/', v.simplemap),
    url(r'^paramap/(?P<year>[0-9]{4})', v.paramap),
   
    #handler404 = v.page_not_found
    url(r'my404', v.my404),
    
    url(r'^redirect/', v.redit_1),
    url(r'^redirect2/', v.redit_2),
    url(r'^dest/', v.dest, name="d1"),
    
    url(r'getinfo', v.getinfo),

    url(r'post_get', v.post_get),
    url(r'post_post', v.post_post),
    
    url(r'myrender', v.myrender),
    url(r'myrender_to_rsp', v.myrender_to_rsp),
    url(r'myredirect', v.myredirect),

    url(r'myview', v.MyView.as_view()),
    
    #url带2个无名参数
    #该方式可以运行，但是不推荐使用
    #参数没有名称，而且page-x作为参数冗余了
    url(r'^mypage/(page-(\d+)?$)', v.index_1),
 
    #以上方式可改写
    #?:表示忽略后面的一部分内容
    url(r'^mypage2/(?:page-(?P<pn>\d+)?)$', v.index_2),

    #额外参数
    url(r'extra/$', v.extra, {'author':'foxchan', 'version':'1.0'} ),
  
    #子url
    #下面URL不能以$结尾
    url(r'kvm/', include('kvm.urls')),
]
