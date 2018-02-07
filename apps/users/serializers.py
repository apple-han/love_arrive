import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from .models import PhoneVerifyRecord
from love_arrive.settings import REGEX_MOBILE

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    def validate_phone(self, phone):
        '''
        验证手机号
        :param phone:
        :return:
        '''
        # 判断手机号是否注册
        if User.objects.filter(phone=phone).count():
            raise serializers.ValidationError('用户已经存在')

        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, phone):
            raise serializers.ValidationError('手机号码非法')

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if PhoneVerifyRecord.objects.filter(add_time__gt=one_mintes_ago, phone=phone).count():
            raise serializers.ValidationError('距离上一次发送未超过60s')
        return phone

class ForgotSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    def validate_phone(self, phone):
        '''
        验证手机号
        :param phone:
        :return:
        '''
        # 判断手机号是否注册
        if User.objects.filter(phone=phone).count():
            raise serializers.ValidationError('用户已经存在')

        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, phone):
            raise serializers.ValidationError('手机号码非法')

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=20, seconds=0)
        if PhoneVerifyRecord.objects.filter(add_time__gt=one_mintes_ago, phone=phone).count():
            raise serializers.ValidationError('距离上一次发送未超过60s')
        return phone

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = "__all__"

class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4,
                                 min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名",help_text="用户名", required=True,allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # 验证码的信息验证
    def validate_code(self, code):
        verify_records = PhoneVerifyRecord.objects.filter(Q(phone=self.initial_data['username']) & Q(code_type='register')).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=20, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["phone"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "phone", "password")

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "gender","image","click_num")


class ForgotPwSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4,
                                 min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")

    phone = serializers.CharField(max_length=11)


    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码"
    )
    repassword = serializers.CharField(
        style={'input_type': 'password'}, help_text="重复密码", label="重复密码"
    )


    def create(self, validated_data):
        # user = super(ForgotPwSerializer, self).create(validated_data=validated_data)
        # #user.set_password(validated_data['password'])
        # password = user.set_password(validated_data['password'])
        # User.objects.filter(phone=validated_data['phone']).update(password=password)
        # #user.save()
        # return user
        user = User(
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])

        User.objects.filter(phone=validated_data['phone']).update(password=user.password)
        return user

    def validate_phone(self, phone):
        # 验证手机号是否已经注册

        print(User.objects.filter(phone=phone).count())
        if User.objects.filter(phone=phone).count() == 0:
            raise serializers.ValidationError('用户不存在 请先注册')

        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, phone):
            raise serializers.ValidationError('手机号码非法')

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if PhoneVerifyRecord.objects.filter(add_time__gt=one_mintes_ago, phone=phone).count():
            raise serializers.ValidationError('距离上一次发送未超过60s')
        return phone

    # 验证两次输入的密码是否一致
    def validate_repassword(self, repassword):
        if repassword != self.initial_data['password'] :
            raise serializers.ValidationError('两次密码不同请重新输入')


    # 验证码的信息验证
    def validate_code(self, code):
        verify_records = PhoneVerifyRecord.objects.filter(
            Q(phone=self.initial_data['phone']) & Q(code_type='forgetpw')).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=20, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        #attrs["phone"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("code", "phone", "password","repassword")

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


