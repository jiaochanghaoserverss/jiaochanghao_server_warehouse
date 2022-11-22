from ronglian_sms_sdk import SmsSDK #导入短信

class Rly_code():
    def __init__(self):
        self.accId = '8aaf07087bc82708017bf7cf8ab00eac'
        self.accToken = 'b9e57dc54f4c4879afa9609f68d2b58d'
        self.appId = '8aaf07087bc82708017bf7cf8bb20eb3'
    def send_message(self,mobile, code, time):
        import json
        sdk = SmsSDK(self.accId, self.accToken, self.appId)
        tid = '1'
        datas = (code, time)
        resp = sdk.sendMessage(tid, mobile, datas)
        result = json.loads(resp)
        if result['statusCode'] == '000000':
            return 1
        return 2
rly = Rly_code()
rly.send_message('18595604641','122222','2003-07-16')