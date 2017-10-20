# -*- coding: utf-8 -*-
'''
Create on 2017年08月27日 18:12

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''


import json
import datetime

from tornado import gen, web

from controller.base import BaseHandler

from service.app_service import AppService


from utils.ips import IP





# 创建应用程序
class CreateAppHandler(BaseHandler):
    def get(self):
        self.render("create_app.html")

    @gen.coroutine
    def post(self):
        user_id = int(self.get_argument("user_id"))
        app_name = self.get_argument("app_name")

        (status, rsp) = yield AppService.create_app(self.application.db_pool, user_id, app_name)


        # 创建应用所需表
        (status2, rsp2) = yield AppService.create_app_table(self.application.db_pool, rsp['data']['appId'])



        # 处理返回值、返回数据
        self.set_header('content-type', 'text/html')
        rsp = self.set_res_data("Register", status, rsp['msg'], rsp['data'])
        # self.finish(rsp)
        return self.render("json_result.html", n1=rsp, )


# 识别用户
class IdentifyServiceHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        # 获取请求参数
        app_key = self.get_argument("app_key")
        # 设备信息
        device_info = self.get_argument("device_info")
        user_id = self.get_argument("user_id")
        platform = int(self.get_argument("platform"))
        user_property = self.get_argument("user_property")  # json类型

        app_id = yield AppService.query_app(db_pool=self.application.db_pool, app_key=app_key)
        # 1002:  应用不存在
        if app_id == '':
            # 处理返回值、返回数据
            # self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("Identify", 1002, '您还没有注册此应用', {})
            # return self.finish(rsp)
            return self.write_json(rsp)

        print("应用id", app_id)

        # 设备信息
        device_info_object = json.loads(device_info)
        # for di in device_info_object.keys():
        device_md5 = device_info_object["device_md5"]
        # platform = device_info_object["platform"]
        device_type = device_info_object["device_type"]
        l = device_info_object["l"]
        h = device_info_object["h"]
        device_brand = device_info_object["device_brand"]
        device_model = device_info_object["device_model"]
        resolution = device_info_object["resolution"]
        imei = device_info_object["imei"]
        mac = device_info_object["mac"]
        is_prison_break = device_info_object["is_prison_break"]
        is_crack = device_info_object["is_crack"]
        languages = device_info_object["language"]
        timezone = device_info_object["timezone"]

        begin_date = datetime.datetime.now()
        begin_date = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = begin_date

        (status, device_id) = yield AppService.insert_device(self.application.db_pool, app_id, device_md5, platform, device_type, l, h, device_brand,
                                                      device_model,
                                                      resolution, imei, mac, is_prison_break, is_crack, languages,
                                                      timezone, user_id, timestamp, types=1)
        if status == 0:
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("Identify", 1003, '您已经有该设备信息了', {})
            return self.finish(rsp)


        (status, ls_id) = yield AppService.insert_app_user(self.application.db_pool, app_id, user_id, device_id, begin_date, platform)


        property_object = json.loads(user_property)
        for p in property_object.keys():
            print(p, property_object[p], type(p), type(property_object[p]))
            property_name = p
            property_data_type = str(type(property_object[p])).replace('<class \'', '').replace('\'>', '')
            property_value = str(property_object[p])
            property_id = yield AppService.insert_app_user_pro(self.application.db_pool, app_id, user_id, ls_id, property_name, property_data_type,
                                                  property_value, platform)

        print("success")

        rsp = self.set_res_data("Identify", 200, 'success', {})
        return self.write_json(rsp)


# 自定义事件
class TrackServcieHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        # 获取请求参数
        app_key = self.get_argument("app_key")

        user_id = self.get_argument("user_id")

        # 设备信息
        event_info = self.get_argument("event_info")

        # 设备信息
        device_info = self.get_argument("device_info")
        # 设备信息
        device_info_object = json.loads(device_info)
        # for di in device_info_object.keys():
        device_md5 = device_info_object["device_md5"]
        # platform = device_info_object["platform"]
        device_type = device_info_object["device_type"]
        l = device_info_object["l"]
        h = device_info_object["h"]
        device_brand = device_info_object["device_brand"]
        device_model = device_info_object["device_model"]
        resolution = device_info_object["resolution"]
        imei = device_info_object["imei"]
        mac = device_info_object["mac"]
        is_prison_break = device_info_object["is_prison_break"]
        is_crack = device_info_object["is_crack"]
        languages = device_info_object["language"]
        timezone = device_info_object["timezone"]

        # 事件属性
        event_attr = self.get_argument("event_attr")

        platform = int(self.get_argument("platform"))

        event_info = json.loads(event_info)

        # 共有的事件属性
        event_name = event_info["event_name"]
        network = int(event_info["network"])
        mccmnc = event_info["mccmnc"]  # 运营商
        useragent = event_info["useragent"]
        channel = event_info["channel"]
        ip = str(event_info["ip"])
        duration = event_info["duration"]
        utc_date = event_info["utc_date"]

        country = ''
        area = ''
        city = ''

        region = ''

        ip_json = {"ip": ip}
        # ip_json = json.dump(ip_json)
        (country, area, region, city, mccmnc) = IP.checkip(ip=ip_json)

        # if mccmnc ==


        # --------------------------
        app_version = ''
        os = ''
        ov = 0

        website = ''
        current_url = ''
        referrer_url = ''
        bs = ''
        bv = 0
        utm_source = ''
        utm_medium = ''
        utm_campaign = ''
        utm_content = ''
        utm_term = ''

        if platform == 1 or platform == 2:  # Android or IOS
            app_version = event_info["app_version"]
            os = event_info["os"]
            ov = event_info["ov"]


        elif platform == 3:  # JS
            website = event_info["website"]
            current_url = event_info["current_url"]
            referrer_url = event_info["referrer_url"]
            bs = event_info["bs"]
            bv = event_info["bv"]
            utm_source = event_info["utm_source"]
            utm_medium = event_info["utm_medium"]
            utm_campaign = event_info["utm_campaign"]
            utm_content = event_info["utm_content"]
            utm_term = event_info["utm_term"]

        # 异步数据库操作
        app_id = yield AppService.query_app(self.application.db_pool, app_key)
        if app_id == '':
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("Identify", 1002, '您还没有注册此应用', {})
            return self.finish(rsp)

        begin_date = datetime.datetime.now()
        begin_date = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = begin_date
        # 手机设备id
        (status, device_id) = yield AppService.insert_device(self.application.db_pool, app_id, device_md5, platform, device_type, l, h, device_brand, device_model,
                                            resolution, imei, mac, is_prison_break, is_crack, languages, timezone,
                                            user_id, timestamp, types=2)

        utc_date_s = begin_date
        session_id = 1
        begin_day_id = 1
        ls_id = 1

        (status, event_id) = yield AppService.insert_app_event(self.application.db_pool, app_id, device_id, user_id, ls_id, session_id, event_name,
                                                     begin_date, begin_day_id, platform, network, mccmnc, useragent,
                                                     website, current_url, referrer_url, channel, app_version, ip,
                                                     country, area, city, os, ov, bs, bv, utm_source, utm_medium,
                                                     utm_campaign, utm_content, utm_term, duration, utc_date_s)
        # if status == 0:
        #     # 处理返回值、返回数据
        #     self.set_header('content-type', 'application/json')
        #     rsp = self.set_res_data("Identify", 1005, '该事件已经注册过了', {})
        #     return self.finish(rsp)



        event_attr_object = json.loads(event_attr)
        for p in event_attr_object.keys():
            print(p, event_attr_object[p], type(p), type(event_attr_object[p]))
            attr_name = p
            attr_data_type = str(type(event_attr_object[p])).replace('<class \'', '').replace('\'>', '')
            attr_value = str(event_attr_object[p])

            yield AppService.insert_app_event_pro(self.application.db_pool, app_id, event_id, device_id, user_id, ls_id, session_id, event_name, attr_name,
                                    attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s)


        rsp = self.set_res_data("Track", 200, 'success', {})
        return self.write_json(rsp)


# 开始事件
class StartTrackServcieHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        # 获取请求参数
        app_key = self.get_argument("app_key")

        user_id = self.get_argument("user_id")

        # 设备信息
        event_info = self.get_argument("event_info")

        # 设备信息
        device_info = self.get_argument("device_info")
        # 设备信息
        device_info_object = json.loads(device_info)
        # for di in device_info_object.keys():
        device_md5 = device_info_object["device_md5"]
        # platform = device_info_object["platform"]
        device_type = device_info_object["device_type"]
        l = device_info_object["l"]
        h = device_info_object["h"]
        device_brand = device_info_object["device_brand"]
        device_model = device_info_object["device_model"]
        resolution = device_info_object["resolution"]
        imei = device_info_object["imei"]
        mac = device_info_object["mac"]
        is_prison_break = device_info_object["is_prison_break"]
        is_crack = device_info_object["is_crack"]
        languages = device_info_object["language"]
        timezone = device_info_object["timezone"]

        # 事件属性
        event_attr = self.get_argument("event_attr")

        platform = int(self.get_argument("platform"))

        event_info = json.loads(event_info)

        # 共有的事件属性
        event_name = event_info["event_name"]
        network = int(event_info["network"])
        mccmnc = event_info["mccmnc"]  # 运营商
        useragent = event_info["useragent"]
        channel = event_info["channel"]
        ip = str(event_info["ip"])
        duration = 0 #event_info["duration"]
        utc_date = event_info["utc_date"]

        country = ''
        area = ''
        city = ''

        region = ''

        ip_json = {"ip": ip}
        # ip_json = json.dump(ip_json)
        (country, area, region, city, mccmnc) = IP.checkip(ip=ip_json)

        # if mccmnc ==


        # --------------------------
        app_version = ''
        os = ''
        ov = 0

        website = ''
        current_url = ''
        referrer_url = ''
        bs = ''
        bv = 0
        utm_source = ''
        utm_medium = ''
        utm_campaign = ''
        utm_content = ''
        utm_term = ''

        if platform == 1 or platform == 2:  # Android or IOS
            app_version = event_info["app_version"]
            os = event_info["os"]
            ov = event_info["ov"]


        elif platform == 3:  # JS
            website = event_info["website"]
            current_url = event_info["current_url"]
            referrer_url = event_info["referrer_url"]
            bs = event_info["bs"]
            bv = event_info["bv"]
            utm_source = event_info["utm_source"]
            utm_medium = event_info["utm_medium"]
            utm_campaign = event_info["utm_campaign"]
            utm_content = event_info["utm_content"]
            utm_term = event_info["utm_term"]

        # 异步数据库操作
        app_id = yield AppService.query_app(self.application.db_pool, app_key)
        if app_id == '':
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("startTrack", 1002, '您还没有注册此应用', {})
            return self.finish(rsp)

        begin_date = datetime.datetime.now()
        begin_date = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = begin_date
        # 手机设备id
        (status, device_id) = yield AppService.insert_device(self.application.db_pool, app_id, device_md5, platform,
                                                             device_type, l, h, device_brand, device_model,
                                                             resolution, imei, mac, is_prison_break, is_crack,
                                                             languages, timezone,
                                                             user_id, timestamp, types=2)

        utc_date_s = begin_date
        session_id = 1
        begin_day_id = 1
        ls_id = 1

        (status, event_id) = yield AppService.insert_app_event(self.application.db_pool, app_id, device_id, user_id,
                                                               ls_id, session_id, event_name,
                                                               begin_date, begin_day_id, platform, network, mccmnc,
                                                               useragent,
                                                               website, current_url, referrer_url, channel, app_version,
                                                               ip,
                                                               country, area, city, os, ov, bs, bv, utm_source,
                                                               utm_medium,
                                                               utm_campaign, utm_content, utm_term, duration,
                                                               utc_date_s)
        # if status == 0:
        #     # 处理返回值、返回数据
        #     self.set_header('content-type', 'application/json')
        #     rsp = self.set_res_data("Identify", 1005, '该事件已经注册过了', {})
        #     return self.finish(rsp)



        event_attr_object = json.loads(event_attr)
        for p in event_attr_object.keys():
            print(p, event_attr_object[p], type(p), type(event_attr_object[p]))
            attr_name = p
            attr_data_type = str(type(event_attr_object[p])).replace('<class \'', '').replace('\'>', '')
            attr_value = str(event_attr_object[p])

            yield AppService.insert_app_event_pro(self.application.db_pool, app_id, event_id, device_id, user_id, ls_id,
                                                  session_id, event_name, attr_name,
                                                  attr_data_type, attr_value, begin_date, begin_day_id, platform,
                                                  utc_date_s)

        rsp = self.set_res_data("startTrack", 200, 'success', {})
        return self.write_json(rsp)



# 结束事件
class EndTrackServcieHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        # 获取请求参数
        app_key = self.get_argument("app_key")
        user_id = self.get_argument("user_id")
        event_name = self.get_argument("event_name")


        # 异步数据库操作
        app_id = yield AppService.query_app(self.application.db_pool, app_key)

        if app_id == '':
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("endTrack", 1002, '您还没有注册此应用', {})
            return self.finish(rsp)

        (event_id, begin_date) = yield AppService.query_app_event(self.application.db_pool, app_id, event_name)
        if begin_date == '':
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("endTrack", 1003, '出错了，找不到此应用', {})
            return self.finish(rsp)


        end_date = datetime.datetime.now()
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        time_b = datetime.datetime.strptime(begin_date, "%Y-%m-%d %H:%M:%S")
        time_e = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        duration = (time_e - time_b).seconds

        utc_date_s = str(end_date)

        # cur = self.application.db.cursor()
        (status, event_id) = yield AppService.update_app_event_duration(self.application.db_pool, app_id, event_name, duration, begin_date, utc_date_s)

        rsp = self.set_res_data("endTrack", 200, 'success', {})
        return self.write_json(rsp)



# 应用程序信息
class AppInfoHtmlHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        user_id = self.get_argument("user_id")
        page = int(self.get_argument("page"))

        app_id = 0
        app_name = ""
        user_name = ""
        app_key = ""

        cur = yield self.application.db_pool.execute(
            "SELECT * FROM t_user as user, t_app as app WHERE app.user_id = '%s'" % user_id)
        if cur.rowcount:
            try:
                app_id = cur._rows[0]['app_id']
                app_name = cur._rows[0]['app_name']
                user_id = cur._rows[0]['user_id']
                user_name = cur._rows[0]['user_name']
                app_key = cur._rows[0]['app_key']
            except:
                pass


        print(app_id, app_name, user_id, user_name, app_key)

        log = []
        try:

            cur = yield self.application.db_pool.execute(
                "SELECT * FROM t_user_" + str(app_id) + " as user, t_device_" + str(app_id) + " as device, t_event_all_" + str(app_id) + " as event"
                                                                                              " WHERE"
                                                                                              " device.user_id = user.user_id"
                                                                                              " AND"
                                                                                              " device.device_id = event.device_id"
                                                                                              " LIMIT %d, %d" % (page * 10, 10))

            if cur.rowcount:
                # print(r'len1=', len(cur._rows))
                # print(r'len2=', len(cur._rows[0]))
                for i in range(len(cur._rows)):
                    #     # for j in range(len(cur2._rows[i])):
                    #     #     print(i, cur2._rows[i][j])
                    #
                    #     print('\n')
                    # print(r'ls_id', cur2._rows[0][0])
                    # print(cur._rows[i]['timestamp'], cur._rows[i]['device_model'])
                    string = ""
                    string += app_name
                    string += ","
                    string += str(cur._rows[i]['timestamp'])
                    string += ","
                    string += str(cur._rows[i]['device_model'])
                    string += ","
                    string += str(cur._rows[i]['ip'])
                    string += ","
                    string += str(cur._rows[i]['country'])
                    string += ","
                    string += str(cur._rows[i]['duration'])
                    string += ","
                    string += str(cur._rows[i]['mac'])
                    string += ","
                    string += str(cur._rows[i]['languages'])
                    string += ","
                    log.append(string)
        except:
            log.append("您还没有创建应用")
            pass

        # cur = self.application.db.cursor()
        # (status, rsp) = yield self.do_async_db(user_id)
        # app_id = rsp['app_id']
        # app_name = rsp['app_name']
        # user_name = rsp['user_name']
        #
        # # log = []
        # (status, log) = yield self.do_async_db2(app_id)

        # cur.close()



        # cur2 = self.application.db.cursor()


        # cur2 = self.application.db.cursor()


        # cur2.close()



        # #
        # # cur = self.application.db.cursor()
        # yield cur.execute("SELECT * FROM t_device_" + str(app_id) + " WHERE types = '%d' and user_id = '%s'" % (1, user_id))
        # if cur.rowcount:
        #     print(r'device_id', cur._rows[0][0])


        # yield cur.execute("SELECT * FROM t_event_all_" + str(app_id) + " ")
        # if cur.rowcount:
        #     print(r'event_id', cur._rows[0][0])
        #     print(r'')
        # cur.close()




        # self.application.db.


        # self.render("register.html", title='LogService', )
        self.render("ten_panel.html", title='LogService',
                    appname=app_name,
                    username=user_name,
                    userId = user_id,
                    app_key = app_key,
                    log=log,
                    )
        # self.write("")
        # self.finish()

    @gen.coroutine
    def do_async_db(self, user_id):
        cur = self.application.db.cursor()
        try:
            result = yield cur.execute("SELECT * FROM t_user as user, t_app as app WHERE app.user_id = '%s'" % user_id)
        except:
            pass
        print('db1')
        print(cur.description)

        app_id = 0
        app_name = ""
        user_id = ''
        user_name = ""
        if cur.rowcount:
            # print(r'用户id', cur._rows[0][0])
            # print(r'用户名', cur._rows[0][1])
            # print(r'应用id', cur._rows[0][5])
            # print(r'应用名称', cur._rows[0][7])
            try:
                app_id = cur._rows[0][0]
                app_name = cur._rows[0][1]
                user_id = cur._rows[0][5]
                user_name = cur._rows[0][7]
            except:
                pass

        # if app_id == 0:
        #     self.render("ten_panel.html", title='LogService',
        #                 appname=app_name,
        #                 username=user_name,
        #                 log=''
        #                 )

        cur.close()

        raise gen.Return((200, {'app_id': app_id,
                                'app_name': app_name,
                                'user_id': user_id,
                                'user_name': user_name,
                                }))

    @gen.coroutine
    def do_async_db2(self, app_id):
        cur2 = self.application.db.cursor()
        sql = "SELECT * FROM t_user_" + str(app_id) + " as user, t_device_" + str(
            app_id) + " as device WHERE device.user_id = user.user_id"
        try:
            result = yield cur2.execute(
                "SELECT * FROM t_user_" + str(app_id) + " as user, t_device_" + str(app_id) + " as device"
                                                                                              " WHERE"
                                                                                              " device.user_id = user.user_id")
        except:
            pass
        print('db2')
        print(cur2.description)
        print(sql)
        log = []
        if cur2.rowcount:
            print(r'len1=', len(cur2._rows))
            print(r'len2=', len(cur2._rows[0]))
            for i in range(len(cur2._rows)):
                #     # for j in range(len(cur2._rows[i])):
                #     #     print(i, cur2._rows[i][j])
                #
                #     print('\n')
                # print(r'ls_id', cur2._rows[0][0])
                print(cur2._rows[i][22], cur2._rows[i][12])
                log.append(str(cur2._rows[i][22]) + "," + cur2._rows[i][12])

        cur2.close()

        raise gen.Return((200, log))