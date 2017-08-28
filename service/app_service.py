# -*- coding: utf-8 -*-
'''
Create on 2017年08月25日 17:16

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''



from tornado import gen, web

from utils.uuids import UUID

import tornado_mysql


class AppService(web.RequestHandler):

    @gen.coroutine
    def create_app(db_pool, user_id, app_name):
        app_key = UUID.generate_UUID(app_name)
        try:
            cur = yield db_pool.execute("INSERT INTO ten_logservice.t_app "
                                  "(app_key, app_name, user_id) VALUES "
                                  "('%s', '%s', '%d')" %
                                   (app_key, app_name, user_id))
            if cur.rowcount > 0:
                # res_set = cur._rows[0]
                app_id = cur.lastrowid
        except:
            print('写入数据库失败')
            # 回滚
            # yield self.application.db.rollback()
            ret = {'msg': '创建失败,应用已存在', 'data': {}}
            return (1001, ret)
        ret = {'msg': '创建成功', 'data': {
            'appId': app_id,
            'appKey': app_key,
            'appName': app_name
        }}
        return (200, ret)

    @gen.coroutine
    def create_app_table(db_pool, app_id):
        if app_id == '':
            return
        # 创建应用所需表
        import tornado_mysql
        try:
            yield db_pool.execute('SELECT * FROM t_device_' + str(app_id))
        except tornado_mysql.ProgrammingError:
            pass
            # --------------------------------------------------------------------------------
            # 设备表
            try:
                yield db_pool.execute('''
                                  DROP TABLE IF EXISTS t_device_''' + str(app_id) + ''';
                                  CREATE TABLE t_device_''' + str(app_id) + ''' (
                                  device_id INTEGER(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                  device_md5 VARCHAR(128) NOT NULL,
                                  platform INTEGER(2) NOT NULL,
                                  device_type VARCHAR(64) NOT NULL,
                                  l INTEGER(4) NOT NULL,
                                  h INTEGER(4) NOT NULL,
                                  device_brand VARCHAR(64) NOT NULL,
                                  device_model VARCHAR(64) NOT NULL,
                                  resolution VARCHAR(64) NOT NULL,
                                  imei VARCHAR(64) NOT NULL,
                                  mac VARCHAR(64) NOT NULL,
                                  is_prison_break INTEGER(2) NOT NULL,
                                  is_crack INTEGER(2) NOT NULL,
                                  languages VARCHAR(64) NOT NULL,
                                  timezone VARCHAR(64) NOT NULL,
                                  user_id VARCHAR(64) NOT NULL,
                                  types INTEGER(2) NOT NULL,
                                  timestamp VARCHAR(32) NOT NULL
                                  );
                                  ''')
            except:
                pass
            # --------------------------------------------------------------------------------
            # 用户属性表
            try:
                yield db_pool.execute('''
                                  DROP TABLE IF EXISTS t_user_property_''' + str(app_id) + ''';
                                  CREATE TABLE t_user_property_''' + str(app_id) + ''' (
                                  property_id INTEGER(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                  user_id VARCHAR(64) NOT NULL,
                                  ls_id INTEGER(8) NOT NULL,
                                  property_name VARCHAR(128) NOT NULL,
                                  property_data_type VARCHAR(128) NOT NULL,
                                  property_value VARCHAR(128) NOT NULL,
                                  platform INTEGER(2) NOT NULL
                                  );
                                  ''')
            except:
                pass
            # --------------------------------------------------------------------------------
            # 用户表
            try:
                yield db_pool.execute('''
                                  DROP TABLE IF EXISTS t_user_''' + str(app_id) + ''';
                                  CREATE TABLE t_user_''' + str(app_id) + ''' (
                                  ls_id INTEGER(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                  user_id VARCHAR(64) NOT NULL,
                                  device_id INTEGER(4) NOT NULL,
                                  begin_date TIMESTAMP NOT NULL,
                                  platform INTEGER(2) NOT NULL
                                  );
                                  ''')
            except:
                pass
            # --------------------------------------------------------------------------------
            # 事件总表
            try:
                # if True:
                yield db_pool.execute('''
                                  DROP TABLE IF EXISTS t_event_all_''' + str(app_id) + ''';
                                  CREATE TABLE t_event_all_''' + str(app_id) + ''' (
                                  event_id INTEGER(4) NOT NULL AUTO_INCREMENT UNIQUE,
                                  device_id INTEGER(4) NOT NULL,
                                  user_id VARCHAR(64) NOT NULL,
                                  ls_id INTEGER(8) NOT NULL,
                                  session_id INTEGER(8) NOT NULL,
                                  event_name VARCHAR(128) NOT NULL,
                                  begin_date TIMESTAMP NOT NULL,
                                  begin_day_id INTEGER(4) NOT NULL,
                                  platform INTEGER(2) NOT NULL,
                                  network INTEGER(2) NOT NULL,
                                  mccmnc VARCHAR(64) NOT NULL,
                                  useragent VARCHAR(64) NOT NULL,
                                  website VARCHAR(64) NOT NULL,
                                  current_url VARCHAR(64) NOT NULL,
                                  referrer_url VARCHAR(64) NOT NULL,
                                  channel VARCHAR(64) NOT NULL,
                                  app_version VARCHAR(64) NOT NULL,
                                  ip VARCHAR(64) NOT NULL,
                                  country VARCHAR(64) NOT NULL,
                                  area VARCHAR(64) NOT NULL,
                                  city VARCHAR(64) NOT NULL,
                                  os VARCHAR(64) NOT NULL,
                                  ov INTEGER(4) NOT NULL,
                                  bs VARCHAR(64) NOT NULL,
                                  bv INTEGER(4) NOT NULL,
                                  utm_source VARCHAR(64) NOT NULL,
                                  utm_medium VARCHAR(64) NOT NULL,
                                  utm_campaign VARCHAR(64) NOT NULL,
                                  utm_content VARCHAR(64) NOT NULL,
                                  utm_term VARCHAR(64) NOT NULL,
                                  duration INTEGER(8) NOT NULL,
                                  utc_date_s VARCHAR(64) NOT NULL,
                                  CONSTRAINT pk_name PRIMARY KEY (user_id, event_name)
                                  );
                                  ''')
            except:
                pass
        return (200, {})


############################################################################################################

    @gen.coroutine
    def query_app(db_pool, app_key):
        cur = yield db_pool.execute("SELECT * FROM ten_logservice.t_app WHERE app_key = '%s'" % app_key)
        if cur.rowcount > 0:
            res_set = cur._rows[0]
            app_id = res_set['app_id']

            return app_id
        else:
            return ''

    @gen.coroutine
    def insert_device(db_pool, app_id, device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id, timestamp, types):
        device_id = 0
        try:
            cur = yield db_pool.execute(
                "INSERT INTO ten_logservice.t_device_" + str(
                    app_id) + " (device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id, types, timestamp) VALUES"
                              " ('%s', '%d', '%s', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%s', '%s', '%d', '%s')" % (
                    device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac,
                    is_prison_break, is_crack, languages, timezone, user_id, types, timestamp))

            if cur.rowcount > 0:
                device_id = cur.lastrowid

        except:
            print('写入数据库失败')
            ret = {'msg': '创建失败', 'data': {}}
            return (0, device_id)

        return (1, device_id)

    @gen.coroutine
    def insert_app_user(db_pool, app_id, user_id, device_id, begin_date, platform):
        ls_id = 0
        cur = yield db_pool.execute(
            "SELECT * FROM ten_logservice.t_user_" + str(
                app_id) + " WHERE user_id = '%s'" % (user_id)
        )

        if cur.rowcount > 0:
            res_set = cur._rows[0]
            ls_id = res_set['ls_id']
            yield db_pool.execute("UPDATE ten_logservice.t_user_" + str(app_id) + " "
                                                                              "SET "
                                                                              "device_id = '%d' "
                                                                              ", "
                                                                              "begin_date = '%s' "
                                                                              ", "
                                                                              "platform = '%d' "
                                                                              "WHERE "
                                                                              "user_id = '%s'" %
                              (device_id, begin_date, platform, user_id))
        else:

            try:
                cur = yield db_pool.execute(
                    "INSERT INTO ten_logservice.t_user_" + str(
                        app_id) + " (user_id, device_id, begin_date, platform) VALUES ('%s', '%d', '%s', '%d')" % (
                    user_id, device_id, begin_date, platform))

                if cur.rowcount > 0:
                    ls_id = cur.lastrowid

            except:

                print('写入数据库失败')
                ret = {'msg': '创建失败', 'data': {}}
                return (1001, ls_id)

        return (200, ls_id)

    @gen.coroutine
    def insert_app_user_pro(db_pool, app_id, user_id, ls_id, property_name, property_data_type, property_value, platform):
        property_id = 0
        cur = yield db_pool.execute("SELECT * FROM ten_logservice.t_user_property_" + str(app_id) +
                          " WHERE ls_id = '%d' AND property_name = '%s' AND user_id = '%s'" %
                          (ls_id, property_name, user_id)
                          )

        if cur.rowcount > 0:
            res_set = cur._rows[0]
            property_id = res_set['property_id']
            yield db_pool.execute("UPDATE ten_logservice.t_user_property_" + str(app_id) +
                              " SET property_name = '%s', property_data_type = '%s', property_value = '%s', platform = '%d' WHERE property_id = '%d' " % (
                                  property_name, property_data_type, property_value, platform, property_id)
                              )
        else:

            try:
                # if True:
                cur = yield db_pool.execute(
                    "INSERT INTO ten_logservice.t_user_property_" + str(
                        app_id) + " (user_id, ls_id, property_name, property_data_type, property_value, platform) VALUES "
                                  "('%s', '%d', '%s', '%s', '%s', '%d')" % (
                        user_id, ls_id, property_name, property_data_type, property_value, platform))

                if cur.rowcount > 0:
                    property_id = cur.lastrowid

            except:
                print('写入数据库失败')
                ret = {'msg': '创建失败', 'data': {}}
                return (1001, ret)

        return (1001, {})


############################################################################################################

    @gen.coroutine
    def insert_app_event(db_pool, app_id, device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network, mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area, city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration, utc_date_s):
        event_id = 0
        cur = yield db_pool.execute("SELECT * FROM ten_logservice.t_event_all_" + str(app_id) +
                          " WHERE ls_id = '%d' AND event_name = '%s' AND user_id = '%s'" %
                          (ls_id, event_name, user_id)
                          )

        if cur.rowcount > 0:
            res_set = cur._rows[0]
            event_id = res_set['event_id']

            yield db_pool.execute("UPDATE ten_logservice.t_event_all_" + str(app_id) + " "
                                                                                   "SET "
                                                                                   "session_id = '%d' "
                                                                                   ", "
                                                                                   "begin_date = '%s' "
                                                                                   ", "
                                                                                   "begin_day_id = '%d' "
                                                                                   ", "
                                                                                   "platform = '%d' "
                                                                                   ", "
                                                                                   "network = '%d' "
                                                                                   ", "
                                                                                   "mccmnc = '%s' "
                                                                                   ", "
                                                                                   "useragent = '%s' "
                                                                                   ", "
                                                                                   "website = '%s' "
                                                                                   ", "
                                                                                   "current_url = '%s' "
                                                                                   ", "
                                                                                   "referrer_url = '%s' "
                                                                                   ", "
                                                                                   "channel = '%s' "
                                                                                   ", "
                                                                                   "app_version = '%s' "
                                                                                   ", "
                                                                                   "ip = '%s' "
                                                                                   ", "
                                                                                   "country = '%s' "
                                                                                   ", "
                                                                                   "area = '%s' "
                                                                                   ", "
                                                                                   "city = '%s' "
                                                                                   ", "
                                                                                   "os = '%s' "
                                                                                   ", "
                                                                                   "ov = '%d' "
                                                                                   ", "
                                                                                   "bs = '%s' "
                                                                                   ", "
                                                                                   "bv = '%d' "
                                                                                   ", "
                                                                                   "utm_source = '%s' "
                                                                                   ", "
                                                                                   "utm_medium = '%s' "
                                                                                   ", "
                                                                                   "utm_campaign = '%s' "
                                                                                   ", "
                                                                                   "utm_content = '%s' "
                                                                                   ", "
                                                                                   "utm_term = '%s' "
                                                                                   ", "
                                                                                   "duration = '%d' "
                                                                                   ", "
                                                                                   "utc_date_s = '%s' "
                                                                                   "WHERE "
                                                                                   "event_name = '%s'" %
                              (session_id, begin_date, begin_day_id, platform, network, mccmnc, useragent, website,
                               current_url, referrer_url, channel, app_version, ip, country, area, city, os, ov, bs, bv,
                               utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration, utc_date_s,
                               event_name))

        else:

            # try:
            if True:
                cur = yield db_pool.execute(
                    "INSERT INTO ten_logservice.t_event_all_" + str(
                        app_id) + " (device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network, mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area, city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration, utc_date_s) VALUES"
                                  " ('%d',      '%s',    '%d',  '%d',       '%s',       '%s',       '%d',         '%d',     '%d',    '%s',   '%s',      '%s',    '%s',        '%s',         '%s',    '%s',       '%s', '%s',  '%s', '%s','%s','%d','%s','%d', '%s',    '%s',       '%s',         '%s',        '%s',     '%d',     '%s')" % (
                        device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network,
                        mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area,
                        city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration,
                        utc_date_s))

                if cur.rowcount > 0:
                    event_id = cur.lastrowid

            # except:
            #
            #     print('写入数据库失败')
            #     ret = {'msg': '创建失败', 'data': {}}
            #     return (0, session_id)

        return (1, event_id)

    @gen.coroutine
    def insert_app_event_pro(db_pool, app_id, event_id, device_id, user_id, ls_id, session_id, event_name, attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s):

        try:
            yield db_pool.execute('SELECT * FROM t_user_event_attr_' + str(app_id) + '_' + str(event_id))
        except tornado_mysql.ProgrammingError:
            print('新建事件属性表...')
            # 事件属性表
            try:
                yield db_pool.execute('''
                                      DROP TABLE IF EXISTS t_user_event_attr_''' + str(app_id) + '''_''' + str(
                    event_id) + ''';
                                      CREATE TABLE t_user_event_attr_''' + str(app_id) + '''_''' + str(event_id) + ''' (
                                      attr_id INTEGER(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                      device_id INTEGER(4) NOT NULL,
                                      user_id VARCHAR(64) NOT NULL,
                                      session_id INTEGER(8) NOT NULL,
                                      event_id INTEGER(4) NOT NULL,
                                      event_name VARCHAR(128) NOT NULL,
                                      ls_id INTEGER(8) NOT NULL,
                                      attr_name VARCHAR(64) NOT NULL,
                                      attr_data_type VARCHAR(64) NOT NULL,
                                      attr_value VARCHAR(128) NOT NULL,
                                      begin_date TIMESTAMP NOT NULL,
                                      begin_day_id INTEGER(4) NOT NULL,
                                      platform INTEGER(2) NOT NULL,
                                      utc_date_s VARCHAR(64) NOT NULL
                                      );
                                      ''')
            except:
                pass

        print("t_user_event_attr_" + str(app_id) + "_" + str(event_id))

        cur = yield db_pool.execute("SELECT * FROM ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) +
                          " WHERE event_name = '%s' AND attr_name = '%s' AND user_id = '%s'" %
                          (event_name, attr_name, user_id)
                          )

        if cur.rowcount > 0:

            res_set = cur._rows[0]
            attr_id = res_set['attr_id']

            yield db_pool.execute("UPDATE ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) +
                              " SET attr_name = '%s', attr_data_type = '%s', attr_value = '%s', begin_date = '%s', begin_day_id = '%d', platform = '%d', utc_date_s = '%s' WHERE attr_id = '%d' " % (
                                  attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s,
                                  attr_id)
                              )

        else:

            try:
                # if True:
                cur = yield db_pool.execute(
                    "INSERT INTO ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) + \
                    " (device_id, user_id, ls_id, session_id, event_id, event_name, attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s) VALUES"
                    " ('%d',      '%s',    '%d',  '%d',       '%s',     '%s',       '%s',      '%s',           '%s',       '%s',       '%d',         '%d',     '%s')" % (
                        device_id, user_id, ls_id, session_id, event_id, event_name, attr_name, attr_data_type,
                        attr_value, begin_date, begin_day_id, platform, utc_date_s))

                if cur.rowcount > 0:
                    session_id = cur.lastrowid

            except:
                print('写入数据库失败')
                ret = {'msg': '创建失败', 'data': {}}
                return (0, session_id)

        return (200, {})


############################################################################################################

    @gen.coroutine
    def query_app_event(db_pool, app_id, event_name):
        event_id = 0
        begin_date = ''
        cur = yield db_pool.execute("SELECT * FROM ten_logservice.t_event_all_" + str(app_id) + " WHERE event_name = '%s'" % event_name)
        if cur.rowcount > 0:
            res_set = cur._rows[0]
            event_id = res_set['event_id']
            try:
                begin_date = str(res_set['begin_date'])
            except:
                import datetime
                begin_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            return (event_id, begin_date)
        else:
            return (0, '')


    @gen.coroutine
    def update_app_event_duration(db_pool, app_id, event_name, duration, begin_date, utc_date_s):
        yield db_pool.execute("UPDATE ten_logservice.t_event_all_" + str(app_id) + " "
                                                                               "SET "
                                                                               "begin_date = '%s', "
                                                                               "duration = '%d', "
                                                                               "utc_date_s = '%s' "
                                                                               "WHERE "
                                                                               "event_name = '%s'" %
                             (begin_date, duration, utc_date_s, event_name))  # begin_date,
        return (200, {})


############################################################################################################
