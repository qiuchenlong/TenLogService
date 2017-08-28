# -*- coding: utf-8 -*-
'''
Create on 2017年08月14日 15:55

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''

import time
import json
from tornado import gen, web


from config import config




'''
所有handler的基类
'''
class BaseHandler(web.RequestHandler):

    def record_log(func):
        def tmp(*args, **kargs):
            print("start %s", time.time())
            ret = func(*args, **kargs)
            print("end %s", time.time())
            # return ret
        return tmp

    '''
    统一返回数据结构
    '''
    @staticmethod
    def set_res_data(action, status=0, msg='success', data=None):
        return_data = {
            "status": status,
            "msg": msg,
            "data": {action: data}
        }
        return json.dumps(return_data)


    def initialize(self):
        self.session = None
        self.db_session = None
        self.seesion_save_tag = False
        self.session_expire_time = 604800 # 7 * 24 * 60 * 60 秒
        self.thread_executor = self.application.thread_executor
        # self.cache_manager = self.application.cache_manager
        self.async_do = self.thread_executor.submit


    # def init_session(self):
    #     if not self.session:
    #         self.session = Session(self)
    #         yield self.session.inin_fetch()


    def write_json(self, json):
        self.set_header("Content-Type", "application/json: charset=UTF-8")
        self.write(json)

    def write_error(self, status_code, **kwargs):
        if not config['debug']:
            if status_code == 403:
                self.render("403.html")
            elif status_code == 404 or 405:
                self.render("404.html")
            elif status_code == 500:
                self.render("500.html")
        if not self._finished:
            super(BaseHandler, self).write_error(status_code, **kwargs)