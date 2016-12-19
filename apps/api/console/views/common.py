# coding=utf-8


from core import messages

from apps import async_response
from apps.api import ApiViewBase
from apps.api.console import auth_login

import settings

class Dashboard(ApiViewBase):
    @async_response
    @auth_login()
    def GET(self):
        return messages.Success

class Launch(ApiViewBase):
    "APP初始化接口"
    @async_response
    def GET(self):
        return 0, 'success', {
            'upload_url_prefix': settings.QINIU.URL_PREFIX,
            'static_url_prefix': '',
        }