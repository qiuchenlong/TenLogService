# -*- coding: utf-8 -*-
'''
Create on 2017年08月24日 16:34

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''


from tornado_mysql import cursors


cookie_keys = dict(
    session_key_name = "TEN_SESSION_ID",
    uv_key_name = "uv_tag",
)


# session相关配置（redis实现）
redis_session_config = dict(
    db_no = 0,
    host = "127.0.0.1",
    port = 6555,
    password = None,
    max_connections = 10,
    session_key_name = cookie_keys['session_key_name'],
    session_expires_days = 7,
)


# 站点缓存(redis)
site_cache_config = dict(
    db_no = 1,
    host = "127.0.0.1",
    port = 6555,
    password = None,
    max_connections = 10,
)


# 数据库配置
detabase_config = dict(
    host = "47.90.50.20",
    port = 3306,
    user = "root",
    passwd = "123456",
    db = "ten_logservice",
    charset = "utf8",
    cursorclass = cursors.DictCursor, #数组转json对象
    max_idle_connections = 3,
    max_recycle_sec = 20,
)


# 站点相关配置以及tornado的相关配置
config = dict(
    debug = False,
    compress_response=True,
    xsrf_cookies = False,
    cookie_secret = "lcdC20BuS5yHcRLscDOI5vhqh85wqkBBtvvEI0T9xtU=",
    login_url = "/index",
    port = 8081,
    max_threads_num = 500,
    database = detabase_config,
)