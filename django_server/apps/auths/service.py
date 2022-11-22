import logging
import random
import re

from apps.auths.models import *
from common.services import BaseService

from common.middles.token import AppTokenService
from utils.redisconn import r
from utils.send_emai.send_email_QQ import Send_email

logger = logging.getLogger(__name__)

# Generate account number
class Users(BaseService):

    @classmethod
    def generate(cls):
        # 生成11位数的账号
        second_spot1 = random.choice([i for i in range(1,10) if i != 6])
        second_spot = random.choice([3, 4, 5, 7, 8])
        third_spot = {3: random.randint(0, 9),
                      4: random.choice([5, 7, 9]),
                      5: random.choice([i for i in range(10) if i != 4]),
                      7: random.choice([i for i in range(10) if i not in [4, 9]]),
                      8: random.randint(0, 9), }[second_spot]
        remain_spot = random.randint(1, 10000000)
        num = "{}{}{}{}".format(second_spot1,second_spot, third_spot, remain_spot)
        return num

class AccountService(BaseService):
    model = User

    @classmethod
    def get_account(cls, pk):
        account = User.objects.get_or_none(pk=pk)
        return account

    @classmethod
    def get_login_token(cls, account):
        token = AppTokenService.create_token(account.id)
        return token

class Code():

    @classmethod
    def send_code(cls, _data):
        # 手机号验证
        if not _data['imguid']:
            return '请填写图形验证码', None
        imguids = str(_data['imguid'])
        if not imguids:
            return '图形验证码不能为空', None
        imguid = r.get_str(_data['uid'])  # 取出图形验证码

        if imguid.lower() == imguids.lower():
            if int(_data['flag']) == 2:
                # 获取号码
                mobile = _data['mobile']
                usermsg = User.objects.filter(mobile=mobile)
                if not usermsg:
                    return '手机号不存在', None
                if mobile:
                    if not mobile:
                        return '手机号不能为空', None
                    mreg = re.match("^1[3-9]\d{9}$", mobile)
                    if not mreg:
                       return '手机号不合法', None
                    mobile_code = r.get_str(mobile)
                    if mobile_code:
                        return '验证码存在，请勿频繁发送', None
                    params = random.randint(100000, 999999)
                    # 容联云发送
                    # res = send(mobile, str(params), 1)
                    # 腾讯云
                    # res = send(mobile,params)
                    res = 1
                    if res:
                        # 发送验证码后存入redis
                        r.set_str(str(mobile), params, 60)
                        return '发送成功', params
            if int(_data['flag']) == 3:
                email = _data['email']
                emails = User.objects.filter(email=email).first()
                if not emails:
                    return '邮箱不存在', None
                if not email:
                    return '邮箱不能为空', None
                email_mreg = re.match(
                    "^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$", email)
                if not email_mreg:
                    return '邮箱不合法', None

                params = random.randint(100000, 999999)
                email_reids = r.get_str(email)
                if email_reids:
                    return '验证码存在，请勿频繁发送', None
                """ 调用邮箱进行发送短信 """
                # try :
                Send_email.send_mail(email, params)
                r.set_str(email, params, 300)
                return '发送成功', params
                # except:
                #     return self.fail_response(None, '发送失败')
        else:
            return '验证码不正确', None
    @classmethod
    def check_code(cls,):
        pass




