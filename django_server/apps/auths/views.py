import json
import random
import re

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response

from utils.qiniuyun import qntoken
from utils.redisconn import r
from utils.send_emai.send_email_QQ import Send_email
from .serial import *
from apps.auths.service import Users, AccountService, Code
from common.views import BaseApiView, BaseModelViewSet, BaseParam, PermLessApiView
from apps.auths.models import *
# 导入redis
from utils.redis_server import get_redis_conn
# 密码加密以及解密
from django.contrib.auth.hashers import make_password, check_password
from utils.check import *
# 导入结果校验

#获取图片验证码
from utils.captcha.captcha import captcha
# 校验 charfile 和整形 以及路由
from rest_framework.decorators import action
from rest_framework.fields import *


class GenerateNumber(PermLessApiView):
    def get(self,request):
        account = Users.generate()
        if User.objects.filter(account=account).first():
            account = Users.generate()
        data = {'account': account}
        return self.success_response(data)

class CreatCaptcha(PermLessApiView):
    def get(self,request):
        #导用cpatcha  text是图片验证码中数字 img是字节流
        name,text,img =captcha.generate_captcha()
        #获取图片验证码 uuid
        uuid = request.GET.get('uuid')
        #保存图形验码
        r.set_str(uuid,text)  #set中前一个参数是键 后一个参数是值
        return HttpResponse(img,content_type='image/jpg')


class SendManage(PermLessApiView):
    def post(self, request):
        # 验证密码
        password = request.data.get("password")
        if not password:
            return self.fail_response(None,'密码不能为空')
        sreg = re.match("\w{5,20}$", password)
        if not sreg:
            return self.fail_response(None,'密码不合法')

        # 验证确认密码
        password1 = request.data.get("confirm_password")
        if not password1:
            return self.fail_response(None,'确认密码不能为空')
        msg = re.match("\w{5,20}$", password1)
        if not msg:
            return self.fail_response(None,'确认密码不合法')
        if password != password1:
            return self.fail_response(None,'密码不一致')
        #获取uid
        uuid = request.data.get('uid')
        #获取图形验证码
        imguids = request.data.get('imguid')
        #开启reids 获取uid的值

        imguid = r.get_str(uuid)  #取出图形验证码
        if not imguids:
            return self.fail_response(None,"请填写验证码")
        if imguid:
            imguid = str(imguid)
            if imguid.lower() == imguids.lower():
                # 获取号码
                mobile = request.data.get("mobile")
                if mobile:
                    mobiles = User.objects.filter(mobile=mobile).first()
                    if mobiles:
                        return self.fail_response(None, '手机号存在')
                    if not mobile:
                        return self.fail_response(None, '手机号不能为空')
                    mreg = re.match("^1[3-9]\d{9}$", mobile)
                    if not mreg:
                        return self.fail_response(None, '手机号不合法')
                    mobile_code = r.get_str(mobile)
                    if mobile_code:
                        return self.fail_response(None,'验证码存在，请勿频繁发送')
                    params = random.randint(100000, 999999)
                    # 容联云发送
                    # res = send(mobile, str(params), 1)
                    # 腾讯云
                    # res = send(mobile,params)
                    res = 1
                    if res :
                        #发送验证码后存入redis
                        r.set_str(str(mobile), params, 60)
                        return self.success_response(params,'发送成功')
                email = request.data.get("email")
                if email:
                    if not email:
                        return self.fail_response(None, '邮箱不能为空')
                    email_mreg = re.match(
                        "^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$", email)
                    if not email_mreg:
                        return self.fail_response(None, '邮箱不合法')
                    emails = User.objects.filter(email=email).first()
                    if emails:
                        return self.fail_response(None, '邮箱存在')
                    code = random.randint(100000,999999)
                    email_reids = r.get_str(email)
                    if email_reids:
                        return self.fail_response(None, '验证码存在，请勿频繁发送')
                    """ 调用邮箱进行发送短信 """
                    # try :
                    Send_email.send_mail(email, code)
                    r.set_str(email, code, 60)
                    return self.success_response(code, '发送成功')
                    # except:
                    #     return self.fail_response(None, '发送失败')
            else:
                return self.fail_response('',"验证码不正确")
        return self.fail_response('',"验证码不存在")

# 验证合法性
class Validate(PermLessApiView):
    def post(self, request):
        # 验证用户名
        name = request.data.get('username')
        # 验证用户名是否为空
        if not name:
            return Response({"code": 10010})
        # 验证用户名是否合法
        reg = re.match("\w{5,10}$", name)
        if not reg:
            return Response({"code": 10011})

        # 验证密码
        password = request.data.get("password")
        if not password:
            return Response({"code": 10016})
        sreg = re.match("\w{5,20}$", password)
        if not sreg:
            return Response({"code": 10017})

        # 验证确认密码
        password1 = request.data.get("confirm_password")
        if not password1:
            return Response({"code": 10020})
        msg = re.match("\w{5,20}$", password1)
        if not msg:
            return Response({"code": 10021})
        if password != password1:
            return Response({"code": 10022})

        # 验证手机号
        mobile = request.data.get("mobiless")
        if not mobile:
            return Response({"code": 10013})
        mreg = re.match("^1[3-9]\d{9}$", mobile)
        if not mreg:
            return Response({"code": 10014})
        mobiles = User.objects.filter(mobile=mobile).first()
        if mobiles:
            return Response({"code": 10015})

        email = request.data.get('emailss')
        if not email:
            return Response({"code": 10041})
        email_mreg = re.match("^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$",email)
        if not email_mreg:
            return Response({"code": 10042})


        # 判断是否同意协议
        # agree = request.data.get('agree')
        # if not agree:
        #     return Response({"code": 10031})
        return Response({"code": 200})
class Register(PermLessApiView):
    def post(self, request):
        account = request.data.get('account')
        # 判断是否同意协议
        agree = request.data.get('user_xy')
        if agree == False:
            return self.fail_response("请勾选协议")
        # 验证用户名
        name = request.data.get('username')
        # 验证用户名是否为空
        if not name:
            return self.fail_response("用户名不能为空")
        # 验证用户名是否合法
        reg = re.match("\w{5,10}$", name)
        if not reg:
            return self.fail_response("用户名不合法")

        # 验证密码
        password = request.data.get("password")
        if not password:
            return self.fail_response("密码不能为空")
        sreg = re.match("\w{5,20}$", password)
        if not sreg:
            return self.fail_response("密码格式不正确")

        # 验证确认密码
        password1 = request.data.get("confirm_password")
        if not password1:
            return self.fail_response("确认密码不能为空")
        msg = re.match("\w{5,20}$", password1)
        if not msg:
            return self.fail_response("确认密码格式不合法")
        if password != password1:
            return self.fail_response("确认密码匹配")

        code = request.data.get('code')

        # 验证手机号
        mobile = request.data.get("mobiless")
        user_mobile = User.objects.filter(mobile=mobile).first()
        if user_mobile:
            return self.fail_response("手机号已存在")
        if mobile:
            if not mobile:
                return self.fail_response("手机号不能为空")
            mreg = re.match("^1[3-9]\d{9}$", mobile)
            if not mreg:
                return self.fail_response("手机号不合法")
            # 获取uid
            uuid = request.data.get('uid')
            # 获取图形验证码
            imguids = request.data.get('Verification_code')
            # 开启reids 获取uid的值
            imguid = r.get_str(uuid)  # 取出图形验证码
            if not imguids:
                return self.fail_response(None, "请填写验证码")
            if imguid:
                imguid = str(imguid)
                if imguid.lower() == imguids.lower():
                    codes = r.get_str(mobile)
                    if not codes:
                        return self.fail_response(None, "请重新发送验证码")
                    if int(code) == int(codes):
                        password = make_password(password)
                        user = User.objects.create(account=account,username=name,password=password,mobile=mobile)
                        user.save()
                        data = {'url':"http://localhost:8080/#/success_response?account="+account+"&username="+name+
                                      "&mobile="+mobile,'msg':200}
                        # url = "http://www.localhost:8080/success_response.com"
                        return self.success_response(data, "注册成功")
                    else:
                        return self.fail_response('验证码不正确')
                else:
                    return self.fail_response('图形验证码不正确')
            else:
                return self.fail_response('请输入图形验证码')

        email = request.data.get('emailss')
        user_email = User.objects.filter(email=email).first()
        if user_email:
            return self.fail_response("邮箱已存在")
        if email:
            if not email:
                return self.fail_response("邮箱不存在")
            email_mreg = re.match("^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$",
                                  email)
            if not email_mreg:
                return self.fail_response("邮箱不合法")
            uuid = request.data.get('uid')
            # 获取图形验证码
            imguids = request.data.get('Verification_code')
            imguid = r.get_str(uuid)  # 取出图形验证码
            if not imguids:
                return self.fail_response(None, "请填写验证码")
            if imguid:
                imguid = str(imguid)
                if imguid.lower() == imguids.lower():
                    codes = r.get_str(email)
                    if int(code) == int(codes):
                        password = make_password(password)
                        user = User.objects.create(account=account, username=name, password=password, email=email)
                        user.save()
                        data = {
                            'url': "http://localhost:8080/#/success_response?account=" + account + "&username=" + name +
                                   "&email=" + email, 'msg': 200}
                        # url = "http://www.localhost:8080/success_response.com"
                        return self.success_response(data, "注册成功")
                    else:
                        return self.fail_response('验证码不正确')
                else:
                    return self.fail_response('图形验证码不正确')

class UserLogin(PermLessApiView):
    def get(self, request):
        params = request.GET
        user = User.objects.filter(Q(account=params['username']) | Q(mobile=params['username']) |
                                   Q(email=params['username']),deleted=False).first()
        if user:
            password = check_password(params['password'],user.password)
            if password:
                token = AccountService.get_login_token(user)
                user_data = {'token':token,'id':user.id,'username':user.username,
                             'account':user.account,'email':user.email,'mobile':user.mobile,'avatar':user.avatar}
                return self.success_response(user_data,"登陆成功")
            else:
                return self.fail_response("账号/密码错误")
        else:
            return self.fail_response("账号/手机号/邮箱不存在")


# 用户中心发送验证码
class UserInfoSend(PermLessApiView):
    def post(self, request):
        #获取uid
        uuid = request.data.get('uid')
        #获取图形验证码
        imguids = request.data.get('imguid')
        #开启reids 获取uid的值

        imguid = r.get_str(uuid)  #取出图形验证码
        if not imguids:
            return self.fail_response(None,"请填写图形验证码")
        if imguid:
            imguid = str(imguid)
            if imguid.lower() == imguids.lower():
                # 获取号码
                mobile = request.data.get("mobile")
                if mobile:
                    mobiles = User.objects.filter(mobile=mobile).first()
                    if mobiles:
                        return self.fail_response(None, '手机号存在')
                    if not mobile:
                        return self.fail_response(None, '手机号不能为空')
                    mreg = re.match("^1[3-9]\d{9}$", mobile)
                    if not mreg:
                        return self.fail_response(None, '手机号不合法')
                    mobile_code = r.get_str(mobile)
                    if mobile_code:
                        return self.fail_response(None,'验证码存在，请勿频繁发送')
                    params = random.randint(100000, 999999)
                    # 容联云发送
                    # res = send(mobile, str(params), 1)
                    # 腾讯云
                    # res = send(mobile,params)
                    res = 1
                    if res :
                        #发送验证码后存入redis
                        r.set_str(str(mobile), params, 60)
                        return self.success_response(params,'发送成功')
                email = request.data.get("email")
                if email:
                    if not email:
                        return self.fail_response(None, '邮箱不能为空')
                    email_mreg = re.match(
                        "^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$", email)
                    if not email_mreg:
                        return self.fail_response(None, '邮箱不合法')
                    emails = User.objects.filter(email=email).first()
                    if emails:
                        return self.fail_response(None, '邮箱存在')
                    code = random.randint(100000,999999)
                    email_reids = r.get_str(email)
                    if email_reids:
                        return self.fail_response(None, '验证码存在，请勿频繁发送')
                    """ 调用邮箱进行发送短信 """
                    # try :
                    Send_email.send_mail(email, code)
                    r.set_str(email, code, 300)
                    return self.success_response(code, '发送成功')
                    # except:
                    #     return self.fail_response(None, '发送失败')
            else:
                return self.fail_response('',"验证码不正确")
        return self.fail_response('',"验证码不存在")

class ForgotPassword(PermLessApiView):
    def get(self, request):
        params = request.GET
        msg, code = Code.send_code(params)
        if code :
            return self.success_response(msg, code)
        else:
            return self.fail_response(msg)

    def post(self, request):
        # 再次验证手机号 账号 邮箱是否正确 正确前端弹出层输入密码 进入put请求进行更改
        _data = request.data
        if int(_data['flag']) == 1:
            user = User.objects.filter(Q(account=_data['account'])).first()
            if not user:
                return self.fail_response("账号不存在")
            return self.success_response(True,'验证成功，正在加载')
        elif int(_data['flag']) == 2:
            imguid = r.get_str(_data['uid'])
            user = User.objects.filter(Q(mobile=_data['mobile'])).first()
            if not user:
                return self.fail_response("手机号暂未被绑定")
            if imguid:
                if not _data['imguid']:
                    return self.fail_response(None, "请填写验证码")
                imguid = str(imguid)
                if imguid.lower() == _data['imguid'].lower():
                    codes = r.get_str(_data['mobile'])
                    if codes:
                        if int(_data['code']) == int(codes):
                            return self.success_response(True,'验证成功，正在加载')
                        else:
                            return self.fail_response("验证码不匹配")
                    else:
                        return self.fail_response("验证码过期")
                else:
                    return self.fail_response("图形验证码不匹配")

        else:
            user = User.objects.filter(Q(email=_data['email'])).first()
            if not user:
                return self.fail_response("邮箱暂未绑定")
            imguid = r.get_str(_data['uid'])
            if imguid:
                if not _data['imguid']:
                    return self.fail_response(None, "请填写验证码")
                imguid = str(imguid)
                if imguid.lower() == _data['imguid'].lower():
                    codes = r.get_str(_data['email'])
                    if codes:
                        if int(_data['code']) == int(codes):
                            return self.success_response(True, '验证成功，正在加载')
                        else:
                            return self.fail_response("验证码不匹配")
                    else:
                        return self.fail_response("验证码过期")
                else:
                    return self.fail_response("图形验证码不匹配")

    def put(self,request):
        # 更改密码
        _date = request.data
        if _date['password'] != _date['password1']:
            return self.fail_response("密码不一致")
        if int(_date['flag']) == 1:
            user = User.objects.filter(Q(account=_date['account']), deleted=False).first()
        elif int(_date['flag']) == 2:
            user = User.objects.filter(Q(mobile=_date['mobile']), deleted=False).first()
        else:
            user = User.objects.filter(Q(email=_date['email']), deleted=False).first()
        if not user:
            return self.fail_response("账户不存在")
        if not check_password(_date['password2'], user.password):
            return self.fail_response("请确认原密码是否一致")
        user.password = make_password(_date['password'])
        user.save()
        return self.success_response(True,'修改成功')


class UpdateUser(BaseModelViewSet):
    queryset = User.objects.all().order_by('id')

    serializer_class = UserSerializer
    edit_serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        _data = request.data
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if int(_data['type']) == 1:
            imguid = r.get_str(_data['uid'])  # 取出图形验证码
            if imguid:
                if not _data['imguid']:
                    return self.fail_response(None, "请填写验证码")
                imguid = str(imguid)
                if _data['email'] == '':
                    del _data["email"]
                else:
                    if imguid.lower() == _data['imguid'].lower():
                        codes = r.get_str(_data['email'])
                        if codes:
                            if int(_data['code']) == int(codes):
                                pass
                            else:
                                return self.fail_response("验证码不匹配")
                        else:
                            return self.fail_response("验证码过期")
                    else:
                        return self.fail_response("图形验证码不匹配")
                if _data['mobile'] == '':
                    del _data["mobile"]
                else:
                    if imguid.lower() == _data['imguid'].lower():
                        codes = r.get_str(_data['mobile'])
                        if int(_data['code']) == int(codes):
                            pass
                        else:
                            return self.fail_response("验证码不匹配")
                    else:
                        return self.fail_response("图形验证码不匹配")
                if _data['avatar'] == '':
                    del _data["avatar"]
        elif _data['type'] == 2:
            del _data["mobile"]
            del _data["email"]

        serializer = self.get_edit_serializer(instance, data=_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return self.success_response('绑定成功')

class QiNiuYun(BaseApiView):
    def get(self,request):
        qiniu_token = qntoken()
        return self.success_response(qiniu_token)










