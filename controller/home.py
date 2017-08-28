# -*- coding: utf-8 -*-
'''
Create on 2017年08月25日 10:17

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''


from controller.base import BaseHandler



class HomeHandler(BaseHandler):
    def get(self):
        self.render("login.html", title='LogService', )