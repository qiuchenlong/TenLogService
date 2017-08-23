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