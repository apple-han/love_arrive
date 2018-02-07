"""love_arrive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from love_arrive.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

#
from users.views import SmsCodeViewset, UserViewset, UserListViewSet, ForgotCodeViewset, ForgotPwViewset,RankViewset
from user_operation.views import UseImageViewset, UsefavViewset,FavuserViewset, MatchFavUserViewSet,EmailView
from goods.views import GoodsViewset,GoodsdetailViewset

router = DefaultRouter()

# 配置用户注册的接口
router.register(r'users', UserViewset, base_name="users")

# 发送短信验证码
router.register(r'codes', SmsCodeViewset, base_name="codes")

# 发送忘记密码短信验证码
router.register(r'forgotcodes', ForgotCodeViewset, base_name="forgotcodes")

# 获取用户的列表
router.register(r'uselist', UserListViewSet, base_name="uselist")

# 获取用户验证照片
router.register(r'images', UseImageViewset, base_name="images")

# 用户关注
router.register(r'userfavs', UsefavViewset, base_name="userfavs")

# 忘记密码
router.register(r'forgotpw', ForgotPwViewset, base_name="forgotpw")

# 关注用户的
router.register(r'favsuser', FavuserViewset, base_name="favsuser")

# 匹配成功的
router.register(r'matchusers', MatchFavUserViewSet, base_name="matchusers")

# 分类商品的列表
router.register(r'categorygoods', GoodsViewset, base_name="categorygoods")

# 分类商品详情接口
router.register(r'categorygoodsdetail', GoodsdetailViewset, base_name="categorygoodsdetail")

# 用户排行榜
router.register(r'rank', RankViewset, base_name="rank")

#
#
#uselist_list = UserListViewSet.as_view({
#     'get': 'list',
# })

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    url(r'docs/', include_docs_urls(title="Love直达")),
    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    url(r'^active/(?P<active_code>.*)/$', EmailView.as_view(), name="user_active"),

]

# 全局500的配置
# handler500 = 'users.views.ServiceUnavailable'
