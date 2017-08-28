# -*- coding: utf-8 -*-
'''
Create on 2017年08月14日 15:00

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''


import controller.user
import controller.app



from tornado.web import url


# url路由
handlers = [
    url(r"/login", controller.user.LoginHandler, name="login"),
    url(r"/register", controller.user.RegisterHandler, name="register"),
    url(r"/create", controller.app.CreateAppHandler, name="create_app"),
    url(r"/api/open/v1/CreateApp", controller.app.CreateAppHandler, name="create_app_api"),
    url(r"/api/open/v1/identify", controller.app.IdentifyServiceHandler, name="identify"),
    url(r"/api/open/v1/track", controller.app.TrackServcieHandler, name="track"),
    url(r"/api/open/v1/startTrack", controller.app.StartTrackServcieHandler, name="startTrack"),
    url(r"/api/open/v1/endTrack", controller.app.EndTrackServcieHandler, name="endTrack"),
    url(r"/panel", controller.app.AppInfoHtmlHandler, name="app_info"),

]




# TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
# STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
#
#
# HANDLERS = [(r'/', LoginHtmlHandler),]
# HANDLERS += [(r'/index', IndexHandler)]
# #(r'/poem', PoemPageHandler)]
#
# HANDLERS += [(r'/result', ResultHtmlHandler)]
#
# HANDLERS += [(r'/login', LoginHtmlHandler)]
# HANDLERS += [(r'/register', RegisterHtmlHandler)]
# # HANDLERS += [(r'/login', LoginHtmlHandler)]
# HANDLERS += [(r'/create_app', CreateAppHtmlHandler)]
# # HANDLERS += [(r'/panel', PanelHtmlHandler)]
#
#
#
# HANDLERS += [(r"/api/open/v1/login", LoginHandler)]
# HANDLERS += [(r"/api/open/v1/Register", RegisterHandler)]
# HANDLERS += [(r"/api/open/v1/CreateApp", CreateAppHandler)]
#
#
# # 识别用户
# HANDLERS += [(r"/api/open/v1/identify", IdentifyServiceHandler)]
# # 自定义事件
# HANDLERS += [(r"/api/open/v1/track", TrackServcieHandler)]
# # 事件时长统计
# HANDLERS += [(r"/api/open/v1/startTrack", StartTrackServcieHandler)]
# HANDLERS += [(r"/api/open/v1/endTrack", EndTrackServcieHandler)]
#
# # 查看信息
# HANDLERS += [(r"/panel", AppInfoHtmlHandler)]