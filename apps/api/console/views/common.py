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
            'static_url_prefix': '',
            'upload_domains': [
                'upload1.amengsms.com',
                'upload2.amengsms.com',
            ]
        }