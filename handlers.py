# -*- coding: utf-8 -*-
'''
Create on 2017年08月14日 15:00

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''


from views import *

import os


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')


HANDLERS = [(r'/', IndexHandler),]
            #(r'/poem', PoemPageHandler)]

HANDLERS += [(r'/result', ResultHtmlHandler)]


HANDLERS += [(r'/register', RegisterHtmlHandler)]
HANDLERS += [(r'/create_app', CreateAppHtmlHandler)]

HANDLERS += [(r"/api/open/v1/Register", RegisterHandler)]
HANDLERS += [(r"/api/open/v1/CreateApp", CreateAppHandler)]

# 识别用户
HANDLERS += [(r"/api/open/v1/identify", IdentifyServiceHandler)]
# 自定义事件
HANDLERS += [(r"/api/open/v1/track", TrackServcieHandler)]
# 事件时长统计
HANDLERS += [(r"/api/open/v1/startTrack", StartTrackServcieHandler)]
HANDLERS += [(r"/api/open/v1/endTrack", EndTrackServcieHandler)]