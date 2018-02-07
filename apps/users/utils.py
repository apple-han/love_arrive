# -*- coding: utf-8 -*-
__author__ = '__apple'
__time__ = '2018/2/3 18:07'

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        if response.status_code == 404:


            response.data['detail'] = "zhidingleimbuunzai"
        response.data['errorCode '] = 10000
    else:
        pass
    return response

