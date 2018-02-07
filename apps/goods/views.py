from django.db.models import Q
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import GoodsSerializer, GoodsDetailSerializer

from .models import Goods
# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class GoodsViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    def retrieve(self, request, *args, **kwargs):
        result = request._request.resolver_match.kwargs['pk']
        goods = Goods.objects.filter(Q(category_id=result) | Q(first_id=result) | Q(second_id=result))
        page = self.paginate_queryset(goods)
        goods_serializer = GoodsSerializer(page, many=True)
        return Response(goods_serializer.data)

class GoodsdetailViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.ListModelMixin):

    queryset = Goods.objects.all()
    serializer_class = GoodsDetailSerializer
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    #
    def retrieve(self, request, *args, **kwargs):
        result = request._request.resolver_match.kwargs['pk']
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        goodsDetail = Goods.objects.filter(id=result)
        goods_serializer = GoodsSerializer(goodsDetail, many=True)
        return Response(goods_serializer.data)





