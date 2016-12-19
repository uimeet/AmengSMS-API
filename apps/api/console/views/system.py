# coding=utf-8

import web

from core import utils, messages
from core.api import enums
from core.libs import cache

from apps import async_response, test
from apps.api import ApiViewBase
from apps.api.console import auth_login

class ClearCache(ApiViewBase):
    "清除缓存"
    @async_response
    @auth_login()
    def POST(self, command):
        handler = getattr(self, '_%s' % command, None)
        if handler:
            return handler()

        return messages.ArgumentInvalid

    def _myrole(self):
        "删除自己的权限缓存"
        cache.manager.delete('UserRole-%s' % web.ctx.admin.id)
        return messages.Success

    def _config(self):
        "系统配置"
        cache.manager.delete('settings-system')
        return messages.Success

    def _allfunctions(self):
        "所有功能列表"
        cache.manager.delete('all-functions')
        return messages.Success

    def _allroles(self):
        "所有角色列表"
        cache.manager.delete('AllRoles')
        return messages.Success