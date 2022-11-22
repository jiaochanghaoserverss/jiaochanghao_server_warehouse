import json
from re import template

# 导入smtp协议  基于tcp协议
import smtplib

# 导入  以二进制发送邮件
from email.mime.text import MIMEText
#                          格式化邮件地址
from email.utils import formataddr
# 到处指定给多个人发送
from email.mime.multipart import MIMEMultipart

from asgiref.sync import async_to_sync

# qq邮箱授权码  blkzjmzkugzibdee

# 封装邮箱发送
# 发给谁  标题  内容
# 针对耗时任务 声明async 关键字   使用 await调用 await awsend_mail('2154195820@qq.com','猜猜我是谁','可以猜的到吗',str(1))

# 发送邮件五大点  to 发送给谁邮箱地址  title 标题  content 内容   id  用户id     _user 自己的邮箱地址   _pwd='' 是点击邮箱设置 用户管理下的smtp打开会给授权码添加在_pwd中

class Send_email():
    @classmethod
    def send_mail(cls, to, code):
        # 发送者
        # _user = "你的邮箱地址"
        _user = '676139664@qq.com'

        # smtp 密钥
        # _pwd = "你刚刚申请的密码"
        _pwd = "blkzjmzkugzibdee"

        # 发送设置
        msg = MIMEMultipart()
        #  标题
        msg['Subject'] = 'You are registering an account：'
        # 谁发的
        msg['Form'] = _user
        # 发给谁
        msg['To'] = to


        # 邮件内容                     http://localhost:8888/active/      http://localhost:8888/emailBack/    html 可以发html , utf-8 html编码
        mail = MIMEText("You are registering your account, please be sure not to disclose the verification code:%s"
                        %str(code), 'html', 'utf-8')
        #   嵌入        把邮件内容嵌入msg中
        msg.attach(mail)

        # 调用 声明 smtp实例     smtp地址    端口号
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)

        # 登录腾讯的邮箱
        #      申请的邮箱地址  , 密钥
        s.login(_user, _pwd)

        # 给目标发送
        #       发送人 , 接收人  ,邮件以字符串形式发送
        s.sendmail(_user, to, msg.as_string())

        # 关闭协议
        s.close()
        return "发送成功"

