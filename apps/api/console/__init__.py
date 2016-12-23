# coding=utf-8

import web
import redirect
from core.api.admin import AdminSession

urls = (
    # APP初始化接口
    '/launch', 'apps.api.console.views.common.Launch',

    # 验证码
    '/verimage', 'apps.common.views.VerImage',
    # 首页
    '/dashboard', 'apps.api.console.views.common.Index',
    # 获取所有有效的菜单
    '/show-menu', 'apps.api.console.views.menu.ShowMenu',

    # === 视频 ===
    # 上传视频接口
    '/video/upload', 'apps.api.console.views.video.Upload',

    # === 管理用户 ===
    # 登录
    '/user/login', 'apps.api.console.views.admin.Login',
    # 登出
    '/user/logout', 'apps.api.console.views.admin.Logout',
    # 管理用户查询
    '/admin/query', 'apps.api.console.views.admin.AdminQuery',
    # 管理用户信息保存
    '/admin/save', 'apps.api.console.views.admin.AdminSave',
    # 管理用户状态变更
    '/admin/(delete|lock|unlock)', 'apps.api.console.views.admin.AdminStatusChange',
    # 获取管理用户信息
    '/admin/get', 'apps.api.console.views.admin.AdminGet',

    # 获取所有可授权功能点
    '/function/all', 'apps.api.console.views.auth.FunctionGetAll',

    # 保存角色信息
    '/role/save', 'apps.api.console.views.auth.RoleSave',
    # 获取给定角色信息
    '/role/get', 'apps.api.console.views.auth.RoleGet',
    # 获取所有角色
    '/role/all', 'apps.api.console.views.auth.RoleGetAll',
    # 删除角色
    '/role/delete', 'apps.api.console.views.auth.RoleDelete',

    # ====== 任务相关 ======
    # 任务查询
    '/task/query', 'apps.api.console.views.task.Query',
    # 任务激活
    '/task/reactive', 'apps.api.console.views.task.Reactive',
    # 获取给定任务详情
    '/task/detail', 'apps.api.console.views.task.Detail',

    # ====== 系统相关 ======
    # 清除缓存
    '/system/cache/clear/([a-z0-9]+)', 'apps.api.console.views.system.ClearCache',
)

app = web.application(urls, locals())

def auth_login(auth_codes=None):
    """
    验证管理后台的登录状态
    @auth_codes str/list/tuple 访问所需的权限码
        如果不提供则只需验证是否登录
    """

    def proxy(func):
        '''
        验证登录状态的装饰器，用到管理后台视图中
        '''

        def wrapper(iself, *args, **kw):
            # 获取管理员会话
            web.ctx.admin = AdminSession.current(app = True)
            if web.ctx.admin.is_auth():
                # 权限判断
                if auth_codes is None or web.ctx.admin.auth.any(auth_codes):
                    return func(iself, *args, **kw)

                return 403, u'您无权限执行该操作'

            return 401, u'登录超时或账号已在其它地方登录'

        return wrapper

    return proxy