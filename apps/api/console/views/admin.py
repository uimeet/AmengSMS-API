# coding=utf-8

import web

from core import utils, messages
from core.libs import verimage
from core.api import admin, enums

from apps import async_response, test
from apps.api import ApiViewBase
from apps.api.console import auth_login

class AdminGet(ApiViewBase):
    "获取管理用户信息"
    @async_response
    @auth_login('admin_manage')
    def GET(self):
        inp = utils.Input()

        admin_id = inp.int('admin_id')
        if admin_id <= 0:
            return messages.ArgumentInvalid

        # 获取管理员信息
        ad = admin.Administrator.find_by_id(admin_id)
        if not ad:
            return messages.NotFound

        del ad.passwd

        actived_role_ids = []
        # 获取起角色信息
        ro = web.ctx.admin.auth.find_user_auths(admin_id)
        if ro:
            actived_role_ids = ro.get_roles().keys()

        # 获取所有角色
        roles = web.ctx.admin.auth.find_roles()
        if roles:
            for r in roles:
                r.actived = r.id in actived_role_ids

        return 0, 'success', {
            'roles': roles,
            'admin': ad,
        }

class AdminStatusChange(ApiViewBase):
    "管理用户状态变更"
    @async_response
    @auth_login('admin_manage')
    def POST(self, command):
        inp = utils.Input()

        admin_id = inp.int('admin_id')
        if admin_id <= 0:
            return messages.ArgumentInvalid

        if admin_id == 1:
            return 1, u'该操作对此类用户无效'

        if command == 'delete':
            result = admin.Administrator.delete(admin_id)
        elif command == 'lock':
            result = admin.Administrator.lock(admin_id)
        elif command == 'unlock':
            result = admin.Administrator.set_status(admin_id, enums.Administrator.Status.Normal.value)

        if result:
            return messages.Success

        return messages.NoOperation

class AdminSave(ApiViewBase):
    "保存给定管理用户"
    @async_response
    @auth_login('admin_manage')
    def POST(self):
        inp = utils.Input()

        admin_id = inp.int('admin_id')
        if admin_id < 0:
            return messages.ArgumentInvalid

        login_name = inp.login_name
        if not login_name:
            return 1, u'请输入登录名'

        role_ids = inp.json('role_ids')
        if admin_id > 0:
            result = admin.Administrator.update(admin_id, login_name, inp.passwd, role_ids, qq = inp.qq, mobile = inp.mobile)
        else:
            result = admin.Administrator.add(login_name, inp.passwd, role_ids, qq = inp.qq, mobile = inp.mobile)

        return result.value, result.text

class AdminQuery(ApiViewBase):
    "管理用户查询"
    @async_response
    @auth_login('admin_manage')
    def GET(self):
        inp = utils.Input()

        result = admin.Administrator.query(inp.login_name, inp.int('role_id'), inp.offset, inp.limit)
        if result:
            result.page = inp.page
            result.offset = inp.offset
            result.limit = inp.limit

            return 0, 'success', result

        return messages.NotFound

class Logout(ApiViewBase):
    "用户登出"
    @async_response
    def POST(self):
        admin.AdminSession.logout()
        return messages.Success

class Login(ApiViewBase):
    "用户登录"
    @test
    def GET(self):
        return self.POST()

    @async_response
    def POST(self):
        ipt = utils.Input()

        if verimage.ImageChar.check(ipt.vercode):
            code = admin.login(ipt.name, ipt.passwd, ipt.vercode, cookie = False, app = True, remember = ipt.boolean('remember'))
            if isinstance(code, (str, unicode)):
                return 500, code
            elif isinstance(code, web.utils.storage):
                return 0, 'success', {
                    'id': code.id,
                    'hash_id': code.hash_id,
                    'name': code.login_name,
                    'status': code.status,
                    'authorized_key': code.authorized_key,
                }
        else:
            return 500, u'验证码错误'