# coding=utf-8

import web
from web.utils import storage

from core import utils, messages
from core.api import video

from apps import async_response
from apps.api import ApiViewBase

class Upload(ApiViewBase):
    "上传视频"
    @async_response
    def POST(self):
        params = {k.replace('file_', ''): v for k, v in web.input().iteritems()}
        v = video.VideoDAL.add(storage(params))
        if v:
            return 0, 'success', v

        return messages.NoOperation