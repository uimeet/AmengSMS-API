# coding=utf-8

import web

from core import utils, messages
from core.api import admin, enums

from apps import async_response, test
from apps.api import ApiViewBase
from apps.api.console import auth_login

class RoleDelete(ApiViewBase):
    "删除给定角色"
    @async_response
    @auth_login('role_manage', async = True)
    def POST(self):
        role_id = utils.intval(web.input().get('role_id'))
        if role_id <= 0:
            return messages.ArgumentInvalid

        if web.ctx.admin.auth.delete_role(role_id):
            return messages.Success

        return messages.NoOperation

class RoleGetAll(ApiViewBase):
    "获取所有管理角色"
    @async_response
    @auth_login('role_manage', async = True)
    def GET(self):
        return 0, 'success', web.ctx.admin.auth.find_roles()

class RoleSave(ApiViewBase):
    "保存给定角色"
    @async_response
    @auth_login('role_manage', async = True)
    def POST(self):
        inp = utils.Input()

        role_id = inp.int('role_id')
        if role_id < 0:
            return messages.ArgumentInvalid

        role_name = inp.name
        if not role_name:
            return messages.ArgumentInvalid

        func_ids = inp.json('func_ids')
        if role_id > 0:
            result = web.ctx.admin.auth.update_role(role_id, role_name, func_ids)
        else:
            result = web.ctx.admin.auth.add_role(role_name, func_ids)

        result = enums.Auth.RoleSaveResult.find(result)
        return result.value, result.text

class RoleGet(ApiViewBase):
    "获取给定角色"
    @async_response
    @auth_login('role_manage', async = True)
    def GET(self):
        inp, me = utils.Input(), web.ctx.admin
        # 角色内码
        role_id = inp.int('role_id')
        if role_id <= 0:
            return messages.ArgumentInvalid

        role = me.auth.find_role_by_id(role_id)
        if not role:
            return messages.NotFound

        # 改角色所有激活的授权码
        actived_function_ids = [func['id'] for func in role['functions']]

        result = {}
        funcs = me.auth.find_all_functions()
        for func_type, funcs in funcs.iteritems():
            pfunc = result.get(func_type)
            if pfunc is None:
                ftype = enums.Auth.FunctionType.find(func_type)
                # 如果没有找到对应的授权功能类型
                # 跳过处理
                if ftype == enums.Auth.FunctionType.Unknown:
                    continue

                result[func_type] = {'children': []}
                result[func_type].update(ftype)

            for func in funcs:
                func.actived = func.id in actived_function_ids
                del func.code
                # 添加到对应功能类型的子列表中
                result[func_type]['children'].append(func)

        return 0, 'success', {
            'role': {
                'id': role['id'],
                'name': role['name'],
            },
            'functions': result.values(),
        }

class FunctionGetAll(ApiViewBase):
    "获取所有可授权功能点"
    @async_response
    @auth_login('role_manage', async = True)
    def GET(self):
        me = web.ctx.admin

        result = {}
        funcs = me.auth.find_all_functions()
        for func_type, funcs in funcs.iteritems():
            pfunc = result.get(func_type)
            if pfunc is None:
                ftype = enums.Auth.FunctionType.find(func_type)
                # 如果没有找到对应的授权功能类型
                # 跳过处理
                if ftype == enums.Auth.FunctionType.Unknown:
                    continue

                result[func_type] = { 'children': [] }
                result[func_type].update(ftype)

            for func in funcs:
                del func.code
                # 添加到对应功能类型的子列表中
                result[func_type]['children'].append(func)

        return 0, 'success', result.values()