# -*- coding: utf-8 -*-
'''
Create on 2017年08月25日 09:58

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''

from tornado import gen, web

from controller.base import BaseHandler

from service.user_service import UserService






class LoginHandler(BaseHandler):
    def get(self):
        self.render("user/login.html", )

    @gen.coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        cursor = yield self.application.db_pool.execute(r"SELECT * FROM t_user WHERE user_name = '%s'" % username)
        if cursor.rowcount:
            res_set = cursor._rows[0]
            user_id = res_set['user_id']
            user_password = res_set['user_password']

            if user_password == password:
                self.redirect('/panel?user_id=%d&page=%d' % (user_id, 0))
            else:
                self.redirect('/login')
        else:
            self.redirect('/login')


class RegisterHandler(BaseHandler):
    def get(self):
        self.render("user/register.html", )

    @gen.coroutine
    def post(self):
        phoneNum = self.get_argument("phoneNum")
        username = self.get_argument("username")
        email = self.get_argument("email")
        password = self.get_argument("password")
        # 异步数据库操作
        # status, rsp = 200, {}
        # result = yield self.async_do(UserService.register_user, self.application.db_pool, phoneNum, username, email, password)
        (status, rsp) = yield UserService.register_user(self.application.db_pool, phoneNum, username, email, password)
        # 处理返回值、返回数据
        self.set_header('content-type', 'text/html')
        rsp = self.set_res_data("Register", status, rsp['msg'], rsp['data'])
        # self.finish(rsp)
        return self.render("json_result.html", n1=rsp, )






