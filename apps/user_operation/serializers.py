from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserImage
from .models import UserConcernlove
from users.serializers import UserDetailSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
class UserimageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserImage
        fields = ("user", "file", "id", "add_time")


class UserFavDetailSerializer(serializers.ModelSerializer):
    concertuser = UserDetailSerializer()
    class Meta:
        model = UserConcernlove
        fields = ("concertuser", "id")

class UserFavSerializer(serializers.ModelSerializer):

    userConcern = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserConcernlove
        validators = [
            UniqueTogetherValidator(
                queryset=UserConcernlove.objects.all(),
                fields=('userConcern','concertuser'),
                message="已经喜欢"
            )
        ]

        fields = ("userConcern","concertuser","id")

# 喜欢当前用户的
class FavUserSerializer(serializers.ModelSerializer):
    userConcern = UserDetailSerializer()
    class Meta:
        model = UserConcernlove
        fields = ("userConcern", "id")

# 匹配成功的用户
class MatchUserSerializer(serializers.ModelSerializer):
    userConcern = UserDetailSerializer()
    class Meta:
        model = UserConcernlove
        fields = ("userConcern", "id")






