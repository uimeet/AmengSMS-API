# coding=utf-8

import web

from core import utils, messages
from core.api import book, enums
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

    def _promotion(self):
        "删除推荐列表的缓存"
        # 获取所有推荐列表id
        ids = book.Book.find_all_promotion_ids()
        if ids:
            # 首页的推荐列表缓存
            ids.append('2,3,4,5,6,7,8,9')
            for pid in ids:
                cache.manager.delete('GetPromotion-%s' % pid)

        return messages.Success

    def _toplist(self):
        "删除排行榜的缓存"
        for name in enums.Book.TopListNames:
            cache.manager.delete('GetTopList-%s' % name)

        return messages.Success