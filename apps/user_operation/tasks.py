# -*- coding: utf-8 -*-
__author__ = '__apple'
__time__ = '2018/1/30 11:21'


from love_arrive.celery import app

@app.task
def send_info_email(email):
    pass