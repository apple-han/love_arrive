from django.shortcuts import render

#Create your views here.
from datetime import datetime

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.cache import cache
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
#from rest_framework_extensions.cache.mixins import CacheResponseMixin
from random import choice
from rest_framework import permissions
from django_redis import get_redis_connection
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import (SmsSerializer, UserRegSerializer, UserDetailSerializer,
                          UserSerializer, ForgotSmsSerializer, ForgotPwSerializer,RankSerializer)
#from love_arrive.settings import APIKEY
from utils.yunpian import YunPian
from utils.permissions import IsOwnerOrReadOnly
from .models import PhoneVerifyRecord

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class Send_code(object):
    def generate_code(self):
        """
        生成四位的验证码
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)
    def send_code_datail(self, send_type='register'):
        yun_pian = YunPian(APIKEY)
        code =self.generate_code()
        sms_status = yun_pian.send_sms(code=code, phone=self.phone)

        print(sms_status)
        if sms_status["code"] != 0:
            return Response({
                "phone":sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = PhoneVerifyRecord(code=code, phone=self.phone,code_type=send_type)
            code_record.save()
            return Response({
                'phone':self.phone
            }, status=status.HTTP_201_CREATED)

class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet, Send_code):
    '''
        发送短信验证码
    '''
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.phone = serializer.validated_data['phone']
        return super().send_code_datail()


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    用户
    '''

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
            #return UserDetailSerializer

        return UserDetailSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["phone"] = user.phone if user.phone else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

class UsersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class UserListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    # '''
    # 用户列表页
    # '''
    # queryset = User.objects.get(id=1)
    # print(queryset)
    # serializer_class = UserSerializer
    # pagination_class = UsersPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ForgotCodeViewset(CreateModelMixin, viewsets.GenericViewSet, Send_code):
    '''
    忘记密码
    '''
    serializer_class = ForgotSmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.phone = serializer.validated_data['phone']

        return super().send_code_datail(send_type='forgetpw')

class ForgotPwViewset(viewsets.GenericViewSet,mixins.UpdateModelMixin,CreateModelMixin):
    '''
    重置密码
    '''
    serializer_class = ForgotPwSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        phone = serializer.validated_data['phone']
        return Response({
            'phone': phone
        }, status=status.HTTP_201_CREATED)


import pickle
class RankViewset(mixins.ListModelMixin,viewsets.GenericViewSet):

    queryset = ''
    serializer_class = RankSerializer

    def list(self, request, *args, **kwargs):
        con = get_redis_connection('default')
        if con.get('rank'):
            queryset = pickle.loads(con.get('rank'))
        else:
            queryset = User.objects.order_by('-click_num')[:10]
            con.set('rank', pickle.dumps(queryset))
            con.expire('rank', 18000)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



# def page_error(request):
#     #全局500处理函数
#     ServiceUnavailable()



