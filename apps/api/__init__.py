# coding=utf-8

import web

from apps.api.console import app as console_app

import settings

urls = (
    # ==== 管理接口 ====
    '/console', console_app,

)

app = web.application(urls, locals())

def loadhook():
    # 存在于允许列表的才可以跨域,否则禁止跨域
    request_domain = web.ctx.env.get('HTTP_ORIGIN')
    if request_domain in settings.CORS_DOMAINS:
        web.header('Access-Control-Allow-Origin', request_domain)
        # 客户端也需要配置 withCredentials 需用到cookie 且增强安全性
        # 注意, 使用认证方式 Access-Control-Allow-Origin 不能为*
        web.header("Access-Control-Allow-Credentials", "true")
        # authorized_key 为验证header必须加入才能跨域,如有其它自定义header也需要加入
        web.header("Access-Control-Allow-Headers",
                   "x-requested-with, content-type, accept, authorized-key, content-type, origin, client")
        # 告诉请求对象验证有效时长，在接下来的1728000秒（20天）不用再发送OPTIONS请求验证合法性。
        web.header('Access-Control-Max-Age', '1728000')

app.add_processor(web.loadhook(loadhook))

class ApiViewBase(object):
    "API视图基类"
    def OPTIONS(self, *kargs, **kwargs):
        return ''