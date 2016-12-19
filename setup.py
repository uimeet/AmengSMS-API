# coding=utf-8

import os, sys
import web
import settings

sys.path.append(os.path.join(os.getcwd()))

from core import utils, api
from core.libs import session
from core.libs import template, config, cache
from apps.api import app as api_app

# 配置网站的根路径
# 尝试解决web.seeother跳转不从根路径开始的问题
os.environ['SCRIPT_NAME'] = ''
os.environ['REAL_SCRIPT_NAME'] = ''


def env():
    import json

    return json.dumps({k: str(v) for k, v in web.ctx.env.items()})


urls = (
    '/env', env,

    # Ajax 调用命令
    '/async-cmd/([\w\-]+)', 'apps.common.views.AsyncCommand',
    # 验证码
    '/verimage', 'apps.common.views.VerImage',
    # API
    '/api', api_app,
)


def notfound():
    "404"
    import settings

    return web.notfound(str(settings.RENDER.notfound(show_stats=False)))


def internalerror():
    "500"
    import settings

    return web.internalerror(str(settings.RENDER.internalerror(show_stats=False)))


def loadhook():
    web.ctx.session = web.config._session
    web.ctx.settings = settings
    web.ctx.params = {}
    web.ctx.config = config.config
    web.ctx.cache = cache.manager

bm = web.application(urls, locals())
bm.add_processor(web.loadhook(loadhook))

# 初始化session
session.session_init(bm)
# 初始化模板
template.init({
    #'skin': skin.manager,
    'settings': settings,
    'debug': web.config.debug,
    'ctx': web.ctx,
    'utils': utils,
    'api': api,
})

