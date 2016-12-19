# coding=utf-8

import web
from core import utils

RESPONSE_FIELDS = ('code', 'message', 'data')

def test(func):
    """
    仅用于测试
    """
    def wrapper(self, *args, **kw):
        if web.config.debug:
            return func(self, *args, **kw)

        return None

    return wrapper

def async_response(func):
    """
    异步响应
    """
    def wrapper(self, *args, **kw):
        values = func(self, *args, **kw)
        if not isinstance(values, (tuple, list)):
            values = [values]

        web.header('Content-type', 'application/json')
        data = utils.json_dumps({ RESPONSE_FIELDS[i]: value for i, value in enumerate(values) if i < 3 }, utils.JsonEncoder)
        # 是否提供第四个参数
        # 如果提供了第四个参数, 则是一个 jsonp callback 调用
        if len(values) == 4:
            return '%s(%s)' % (values[3], data)

        return data

    return wrapper