from rest_framework import serializers

from .models import Goods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"

class GoodsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"
