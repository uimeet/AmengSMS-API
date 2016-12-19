# coding=utf-8

import urlparse
import web

import settings
from core import utils

def combine(uri, **kw):
    """
    将给定参数组合到给定uri中
    """
    if kw:
        import urllib
        # 组合参数
        params = urllib.urlencode(kw)
        # uri中是否包含问号，没有就补一个
        if '?' not in uri:
            uri += '?'
        if uri[-1:] != '?':
            uri += '&'

        uri += params

    return uri

def redirect(uri, **kw):
    """
    转向到给定地址
    """
    # 最后再转向
    raise web.seeother(combine(uri, **kw))

def baidu():
    "跳转到百度"
    return redirect('http://www.baidu.com/')

def home():
    "返回首页"
    return redirect('http://%s/home' % web.ctx.host)

def register():
    "返回到注册页"
    return redirect('%s/register' % settings.APP_PREFIX.USER)

def login():
    "返回到登录页"
    return redirect('%s/login' % settings.APP_PREFIX.USER)


def referer(**kwargs):
    """
    跳转到上一页
    """
    # 获取上一页地址
    referer = utils.get_referer()
    if referer:
        u = urlparse.urlparse(referer)
        # 来访页是否是本站
        if not u.netloc or settings.DOMAIN == u.netloc or settings.DOMAIN in u.netloc:
            # 如果是本站，则跳转到该页
            return redirect(referer, **kwargs)
    # 其他情况全部返回首页
    return home()

