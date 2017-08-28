# -*- coding: utf-8 -*-
'''
Create on 2017年08月25日 11:16

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''


from tornado import gen, web


class UserService(web.RequestHandler):


    @gen.coroutine
    def register_user(db_pool, phoneNum, username, email, password):
        try:
            yield db_pool.execute("INSERT INTO ten_logservice.t_user (user_name, user_phone, user_email, user_password) VALUES ('%s', '%s', '%s', '%s')" % (username, phoneNum, email, password))
            # 提交
            # yield self.application.db.commit()
        except:
            print("写入数据库失败")
            # 回滚
            # yield self.application.db.rollback()
            ret = {'msg': '注册失败，用户已存在', 'data': {}}
            return (1001, ret)


        cur = yield db_pool.execute("SELECT * FROM ten_logservice.t_user WHERE user_phone = '%s'" % phoneNum)
        if cur.rowcount > 0:
            res_set = cur._rows[0]
            user_id = res_set['user_id']

        ret = {'msg': '注册成功', 'data': {
            'userId': user_id,
            'username': username,
            'phoneNum': phoneNum,
            'email': email
        }}
        return (200, ret)