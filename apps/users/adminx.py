import xadmin
from xadmin import views
from .models import PhoneVerifyRecord, UserProfile

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "LoveArrive"
    site_footer = "Love"


class PhoneVerifyRecordAdmin(object):
    list_display = ['code', 'phone',"code_type","add_time"]


xadmin.site.register(PhoneVerifyRecord, PhoneVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)