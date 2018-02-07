import xadmin
from xadmin import views
from .models import UserImage, UserConcernlove


class UserImageAdmin(object):
    list_display = ['user', 'file', "addtime"]

class UserConcernloveAdmin(object):
    list_display = ['userConcern', "concertuser", "addtime"]




xadmin.site.register(UserImage, UserImageAdmin)
xadmin.site.register(UserConcernlove, UserConcernloveAdmin)
#xadmin.site.register(MutualConcern, MutualConcernAdmin)
