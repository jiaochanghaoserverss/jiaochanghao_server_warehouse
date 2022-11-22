"""django_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from rest_framework import routers
from apps.auths.views import *

auths_urls = [
    # path('admin/', admin.site.urls),
    path('users/createUser', Register.as_view()),
    # 生成账号
    path('users/generatenumber', GenerateNumber.as_view()),
    # 生成图形验证码
    path('users/creatCaptcha', CreatCaptcha.as_view()),
    # 手机发送短信
    path('users/sendManage', SendManage.as_view()),
    # 验证合法性
    path('users/validate', Validate.as_view()),
    # 用户登陆
    path('users/userlogin', UserLogin.as_view()),
    # 用户中心绑定手机号邮箱 校验
    path('users/userinfosend', UserInfoSend.as_view()),
    path('users/qiniuyun', QiNiuYun.as_view()),
    # 找回密码验证
    path('users/forgotpassword', ForgotPassword.as_view()),

]

user_routers = routers.DefaultRouter(trailing_slash=False)
user_routers.register(r'user/updateuser', UpdateUser)
