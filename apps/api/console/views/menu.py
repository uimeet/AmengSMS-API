# coding=utf-8

import web
from web.utils import storage

from core import messages

from apps import async_response
from apps.api import ApiViewBase
from apps.api.console import auth_login


MENUS = [
    # 用户管理
    storage(text = u'用户', icon = 'ti-user', state = 'console.user', type = 1, children = [
        storage(text = u'用户列表', state = 'console.user.list', code = 'user_manage'),
        storage(text = u'交易记录', state = 'console.user.transaction', code = 'transaction_manage'),
    ]),
    # 管理员管理
    storage(text = u'管理员', icon = 'ti-github', state = 'console.admin', type = 4, children = [
        storage(text = u'账户设置', state = 'console.admin.user', code = 'admin_manage'),
        storage(text = u'管理角色', state = 'console.admin.role', code = 'role_manage'),
    ]),
    storage(text = u'任务中心', icon = 'ti-microsoft-alt', state = 'console.task', type = 99, children = [
        storage(text = u'任务列表', state = 'console.task', code = 'task_manage'),
    ]),
]

class ShowMenu(ApiViewBase):
    "显示所有有效的管理菜单"
    @async_response
    @auth_login(async = True)
    def GET(self):
        menus = []
        admin = web.ctx.admin
        for menu in MENUS:
            codes = admin.auth.filter([m.code for m in menu.children])
            if codes:
                if menu.children:
                    m = storage(text = menu.text, icon = menu.icon, state = menu.state, type = menu.type, children = [])
                    for func in menu.children:
                        if func.code in codes:
                            m.children.append({
                                'text': func.text,
                                'state': func.state,
                                'icon': func.get('icon'),
                            })
                    menus.append(m)
        return 0, 'success', menus