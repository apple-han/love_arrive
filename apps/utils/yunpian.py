import json
import requests

class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, phone):
        parmas = {
            'apikey':self.api_key,
            'mobile':phone,
            "text": "【love直达】您的验证码是{0}".format(code)
        }

        res = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(res.text)
        return re_dict


if __name__ == "__main__":
    yun_pian = YunPian("")
    yun_pian.send_sms("2018", "")