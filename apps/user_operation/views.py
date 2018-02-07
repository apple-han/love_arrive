import re

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils.encoding import smart_text
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework import exceptions

from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from .models import UserImage, UserConcernlove
from utils.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyconcert
from .serializers import (UserimageSerializer, UserFavSerializer, UserFavDetailSerializer,
                          FavUserSerializer,MatchUserSerializer)
from utils.email_send import send_info_email
import json
from django.utils.translation import ugettext as _
import jwt
from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

# Create your views here.
User = get_user_model()
class UseImageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户头像
    create:
        添加用户头像
    delete:
        删除用户功能
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserimageSerializer

    def get_queryset(self):
        return UserImage.objects.filter(user=self.request.user)

class UsefavViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
        list:
            获取用户关注的对象
        retrieve:
            判断某个人用户是否喜欢
        delete:
            取消用户喜欢
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyconcert)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = UserConcernlove.objects.all()
    #serializer_class = UserFavSerializer
    lookup_field = "concertuser_id"

    def get_queryset(self):
        return UserConcernlove.objects.filter(userConcern=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            #email = self.request.POST.concertuser
            return UserFavSerializer

        return UserFavSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user_id = serializer._context['request'].POST['concertuser']
        user = User.objects.get(id=user_id)
        email = User.objects.get(id=user_id).email
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        send_info_email(email,token)
        #headers = self.get_success_headers(serializer.data)
        return Response(serializer.data)

class FavuserViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    喜欢当前用户的接口
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyconcert)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = UserConcernlove.objects.all()
    serializer_class = FavUserSerializer
    lookup_field = "userConcern_id"

    def get_queryset(self):
        return UserConcernlove.objects.filter(concertuser=self.request.user)


class MatchFavUserViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    list:
        获取相互喜欢的对象
    delete:
        取消用户喜欢
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyconcert)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = MatchUserSerializer
    lookup_field = "userConcern_id"
    def get_queryset(self):

        return UserConcernlove.objects.filter(Q(concertuser=self.request.user) & Q(matchsucess='0') )


class EmailView(APIView,BaseJSONWebTokenAuthentication):
    def get(self, request, active_code):
        re_token = re.compile(r'(.*)\*(.*)')
        self.token = re.search(re_token, active_code).group(2)
        json_token = {}
        try:
            payload = jwt_decode_handler(self.token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        json_token['user:'] = user
        # 这里解析token

        return HttpResponse(json.dumps(json_token), content_type="application/json")



    # def authenticate(self):
    #     """
    #     Returns a two-tuple of `User` and token if a valid signature has been
    #     supplied using JWT-based authentication.  Otherwise returns `None`.
    #     """
    #     jwt_value = self.token.encode('utf-8')
    #     if jwt_value is None:
    #         return None
    #
    #     payload = jwt_decode_handler(jwt_value)
    #
    #     user = self.authenticate_credentials(payload)
    #
    #     return (user, jwt_value)












