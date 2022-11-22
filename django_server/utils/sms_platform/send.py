#封装
from utils.sms_platform.ronglianyun.rly import rly
from utils.sms_platform.tengxunyun import txy


def send(type,mobile,params=None,time=None):
    if type == 1:
        rly.send_message(mobile,params,time)
    elif type==2:
        txy.sendsms(mobile,params)
