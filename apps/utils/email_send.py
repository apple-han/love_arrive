# -*- coding: utf-8 -*-
__author__ = '__apple'
__time__ = '2018/1/30 11:30'
#
from random import Random
from django.core.mail import send_mail

from love_arrive.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_info_email(email,token):
    code = random_str(16)
    email_title = "Love直达有人关注你了"
    email_body = ("请点击下面的链接关注对方吧:http://127.0.0.1:8000/active/{code}*{token}"
                                          .format(code=code, token=token))
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass


if __name__ == '__main__':
    send_info_email('1991585851@qq.com',)



