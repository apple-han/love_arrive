import xadmin
from xadmin import views
from .models import  Goods, HotSearchWords,GetIp



class GoodsAdmin(object):
    list_display = ['category_id',"second_id","first_id" "goods_sn", "title","url","brand","click_num","sold_num","fav_num","goods_num"
                    ,"price","goods_brief","goods_desc",
                    "is_new","is_hot","pic","add_time"]

class HotSearchWordsAdmin(object):
    list_display = ['keywords', "index", "add_time"]

class GetIpAdmin(object):
    list_display = ['keywords', "index", "add_time"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(HotSearchWords, HotSearchWordsAdmin)
xadmin.site.register(GetIp, GetIpAdmin)