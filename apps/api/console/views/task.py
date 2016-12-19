# coding=utf-8

import web

from core import utils, messages
from core.api import task, enums

from apps import async_response, test
from apps.api import ApiViewBase
from apps.api.console import auth_login

class Detail(ApiViewBase):
    "获取任务详情"
    @async_response
    @auth_login('task_manage')
    def GET(self):
        inp = utils.Input()
        task_id = inp.int('task_id')

        if task_id <= 0:
            return messages.ArgumentInvalid

        tk = task.TaskDAL.load(task_id)
        if tk is None:
            return messages.NotFound

        # 读取最近5次的执行日志
        logs = task.TaskDAL.get_last_logs(task_id, 5)
        if logs:
            tk.logs = []
            for log in logs:
                log.status = enums.Task.Status.find(log.status)
                log.status_text = utils.json_loads(log.status_text)
                log.status_time = utils.timestamp2date(log.status_time)
                tk.logs.append(log)

        return 0, 'success', tk

class Reactive(ApiViewBase):
    "重新激活给定任务"
    @async_response
    @auth_login('task_manage')
    def POST(self):
        inp = utils.Input()
        task_id = inp.int('task_id')

        if task_id <= 0:
            return messages.ArgumentInvalid

        tk = task.TaskDAL.load(task_id)
        if tk is None:
            return messages.NotFound

        if tk.status != enums.Task.Status.Failure:
            return 2, u'只有状态为处理失败的任务才能重新激活'

        if tk.active():
            return messages.Success

        return messages.NoOperation

class Query(ApiViewBase):
    "查询任务记录"
    @async_response
    @auth_login('task_manage')
    def GET(self):
        inp = utils.Input()

        result = task.TaskDAL.query(inp.int('status'), inp.offset, inp.limit)
        if result:
            result.page = inp.page
            result.offset = inp.offset
            result.limit = inp.limit

            return 0, 'success', result

        return messages.NotFound