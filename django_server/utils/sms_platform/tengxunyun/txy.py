# 发送短信

# 导入腾讯云模块
from qcloudsms_py import SmsSingleSender

# 导入腾讯云指定异常库
from qcloudsms_py.httpclient import HTTPError

# 导入ssl证书
import ssl

ssl._create_default_https_context = ssl.create_default_context


class SendSms:

    def __init__(self):
        # 应用id  appid
        self.appid = 1400601122
        # 应用密钥
        self.appkey = "2300c2d4e0b3a8d1b8dc573c53d0c26a"

        # 短信模板
        self.template_id = 1423825

        # 签名   复制 的是内容
        self.sms_sign = 'python面试总结'

    # 发送短信
    def send_mss(self, mobile,code):

        # 实例化对象
        mysms = SmsSingleSender(self.appid, self.appkey)

        # 通配符模板变量
        params = ['6666']  # 通配符不一定是一个
        # 发送带验证参数的验证码  86 国际区号
        # 区号   手机号     模板id       通配符变量 签名
        try:
            # mysms.send_with_param(86, phone, self.template_id, params, sign=self.sms_sign, extend='', ext='')
            respones = mysms.send_with_param(
                86,
                mobile,
                self.template_id,
                code,
                sign=self.sms_sign,
                extend="", ext=""
            )
            print(respones)

        except HTTPError as e:  # 捕获导入腾讯云指定异常
            # print(str(e))
            pass
        except Exception as e:
            # print(str(e))
            pass


# 实例化对象
sendsms = SendSms()
# sendsms.send_mss('18585604641')

