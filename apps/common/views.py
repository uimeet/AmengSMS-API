# coding=utf-8

import web
from core import utils
from core.libs import verimage, ip


class VerImage(object):
    "验证码"

    def GET(self):
        ic = verimage.ImageChar(fontColor=(100, 211, 90))
        ic.randLetter(4)

        web.ctx.headers.append(('Content-Type', 'image/png'))
        return ic.render().getvalue()


class AsyncCommand(object):
    def GET(self, command):
        return self.execute_command(command)

    def POST(self, command):
        return self.execute_command(command)

    def execute_command(self, command):
        func = getattr(self, '_%s' % command.replace('-', '_'))
        if func:
            return func()
        return None

    def _xloc_init(self):
        """
        位置初始化,用于异步缓存访问客户的位置,便于在需要的时候获取
        :return:
        """
        ip.location()
        return 'var T = %s;' % utils.timestamp()