# -*- coding: utf-8 -*-
'''
Create on 2017年08月14日 15:00

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''
import datetime
import json
import threading

import tornado_mysql
from tornado import gen, web

from controller.BaseHandler import BaseHandler
from utils.ips import IP
from utils.uuids import UUID
lock = threading.Lock()


class IndexHandler(BaseHandler):
    # executor = ThreadPoolExecutor(10)
    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def get(self):
        # ret = json.dumps({"1": 1})
        # self.finish(ret)
        self.render("index.html", title = 'LogService',)

class RegisterHtmlHandler(BaseHandler):
    # executor = ThreadPoolExecutor(10)
    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def get(self):
        # ret = json.dumps({"1": 1})
        # self.finish(ret)
        self.render("register.html", title = 'LogService',)


class ResultHtmlHandler(BaseHandler):
    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def get(self):
        # ret = json.dumps({"1": 1})
        # self.finish(ret)
        self.render("json_result.html", n1='LogService', )



class CreateAppHtmlHandler(BaseHandler):
    # executor = ThreadPoolExecutor(10)
    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def get(self):
        # ret = json.dumps({"1": 1})
        # self.finish(ret)
        self.render("create_app.html", title = 'LogService',)


'''
用户注册
'''
class RegisterHandler(BaseHandler):
    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def post(self):
        # 获取请求参数
        phoneNum = self.get_argument("phoneNum")
        username = self.get_argument("username")
        email = self.get_argument("email")
        password = self.get_argument("password")
        # 异步数据库操作
        (status, rsp) = yield self.do_async_db(phoneNum, username, email, password)
        # 处理返回值、返回数据
        self.set_header('content-type', 'text/html')
        rsp = self.set_res_data("Register", status, rsp['msg'], rsp['data'])
        # self.finish(rsp)
        return self.render("json_result.html", n1=rsp, )


    @gen.coroutine
    def do_async_db(self, phoneNum, username, email, password):
        db_pool = self.application.db_pool
        try:
            yield db_pool.execute("INSERT INTO ten_logservice.t_user (user_name, user_phone, user_email, user_password) VALUES ('%s', '%s', '%s', '%s')" % (username, phoneNum, email, password))
            # 提交
            # yield self.application.db.commit()
        except:
            print("写入数据库失败")
            # 回滚
            # yield self.application.db.rollback()
            ret = {'msg': '注册失败，用户已存在', 'data': {}}
            raise gen.Return((1001, ret))


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
        raise gen.Return((200, ret))


class LoginHtmlHandler(BaseHandler):
    def get(self):
        self.render("login.html", title = 'LogService',)

    @gen.coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        next_url = self.get_argument('next', '/')
        user = None
        # user = yield self.async_do(UserService.get_user, self.db, username)
        if user is not None and user.password == password:
            self.save_login_user(user)
            self.add_message('success', u'登陆成功！欢迎回来，{0}!'.format(username))
            self.redirect(next_url)
        else:
            self.add_message('danger', u'登陆失败！用户名或密码错误，请重新登陆。')
            self.get()

class LoginHandler(BaseHandler):
    # @BaseHandler.record_log
    # @web.asynchronous
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
                self.redirect('/panel?user_id=%d' % user_id)
            else:
                self.redirect('/login')
        else:
            self.redirect('/login')

        # cur = self.application.db.cursor()
        # yield cur.execute(r"SELECT * FROM t_user WHERE user_name = '%s'" % username)
        # if cur.rowcount:
        #     user_id = cur._rows[0][0]
        #     user_password = cur._rows[0][4]
        #
        #     if user_password == password:
        #         self.redirect('/panel?user_id=%d' % user_id)
        #     else:
        #         self.redirect('/login')
        # else:
        #     self.redirect('/login')

        # user = yield self.async_do(UserService.get_user, self.db, username)
        # if user is not None and user.password == password:
            # self.save_login_user(user)
            # self.add_message('success', u'登陆成功！欢迎回来，{0}!'.format(username))
            # self.redirect(next_url)
        # else:
            # self.add_message('danger', u'登陆失败！用户名或密码错误，请重新登陆。')
            # self.get()




class PanelHtmlHandler(BaseHandler):
    def get(self):
        self.render("panel.html", title = 'LogService',)





'''
新建应用
'''
class CreateAppHandler(BaseHandler):
    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def post(self):
        # 获取请求参数
        user_id = int(self.get_argument("user_id"))
        app_name = self.get_argument("app_name")
        # 异步数据库操作
        (status, rsp) = yield self.do_async_db('', app_name, user_id)
        # 1001：应用已经存在
        if status == 1001:
            # 处理返回值、返回数据
            self.set_header('content-type', 'text/html')
            rsp = self.set_res_data("Register", status, rsp['msg'], rsp['data'])
            # return self.finish(rsp)
            return self.render("json_result.html", n1=rsp, )


        # (status, rsp) = yield self.do_async_db('', app_name + '1')
        (status2, rsp2) = yield self.do_async_db2(rsp['data']['appId'])

        # self.do_toto(status, rsp)

        # 提交
        # yield self.application.db.commit()

        # 处理返回值、返回数据
        self.set_header('content-type', 'text/html')
        rsp = self.set_res_data("Register", status, rsp['msg'], rsp['data'])
        # return self.finish(rsp)
        return self.render("json_result.html", n1=rsp, )

    def do_toto(self, status, rsp):
        if status == 200:
            (status, rsps) = yield self.do_async_db2(rsp['data']['appId'])


    @gen.coroutine
    def do_async_db(self, app_id, app_name, user_id):
        app_key = UUID.generate_UUID(app_name)
        cur = self.application.db.cursor()
        # app_id = ''

        try:
            # yield cur.execute('SELECT * FROM ten_logservice.t_app')
            yield cur.execute("INSERT INTO ten_logservice.t_app (app_key, app_name, user_id) VALUES ('%s', '%s', '%d')" % (app_key ,app_name, user_id))

            if cur.rowcount > 0:
                app_id = cur.lastrowid

            # 提交
            # yield self.application.db.commit()



        except:
            print('写入数据库失败')
            # 回滚
            # yield self.application.db.rollback()
            ret = {'msg': '创建失败,应用已存在', 'data': {}}
            raise gen.Return((1001, ret))

        yield cur.close()

        print(app_id)

        # (status, rsp) = yield self.do_async_db2(app_id)


        # t1 = threading.Thread(target=self.fun1, args=(int(app_id),))
        # t1.start()


        # cur2 = self.application.db.cursor()

        # yield cur2.execute(
        #     "SELECT * FROM ten_logservice.t_app WHERE app_name = '%s'" % (app_name))
        # print(cur2.description)
        # yield cur2.execute('''
        #                     DROP TABLE IF EXISTS %s;
        #                     CREATE TABLE %s(
        #                     device_id INTEGER(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        #                     device_md5 VARCHAR(128) NOT NULL,
        #                     platform INTEGER(2) NOT NULL UNIQUE,
        #                     device_type VARCHAR(64) NOT NULL,
        #                     l INTEGER(4) NOT NULL,
        #                     h INTEGER(4) NOT NULL,
        #                     device_brand VARCHAR(64) NOT NULL,
        #                     device_model VARCHAR(64) NOT NULL,
        #                     resolution VARCHAR(64) NOT NULL,
        #                     imei VARCHAR(64) NOT NULL,
        #                     mac VARCHAR(64) NOT NULL,
        #                     is_prison_break INTEGER(2) NOT NULL,
        #                     is_crack INTEGER(2) NOT NULL,
        #                     languages VARCHAR(64) NOT NULL,
        #                     timezone VARCHAR(64) NOT NULL
        #                     );
        #                     ''' % ('t_device_' + str(app_id),
        #                            't_device_' + str(app_id)))

        ret = {'msg': '创建成功', 'data': {
            'appId': app_id,
            'appKey': app_key,
            'appName': app_name
        }}


        raise gen.Return((200, ret))

    # @gen.coroutine
    # def fun1(self, app_id):
    #     print('lalla', app_id)
    #     cur2 = self.application.db.cursor()
    #     yield cur2.execute('''
    #                               DROP TABLE IF EXISTS t_device_''' + str(app_id) + ''';
    #                               CREATE TABLE t_device_''' + str(app_id) + ''' (
    #                               device_id INTEGER(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #                               device_md5 VARCHAR(128) NOT NULL,
    #                               platform INTEGER(2) NOT NULL UNIQUE,
    #                               device_type VARCHAR(64) NOT NULL,
    #                               l INTEGER(4) NOT NULL,
    #                               h INTEGER(4) NOT NULL,
    #                               device_brand VARCHAR(64) NOT NULL,
    #                               device_model VARCHAR(64) NOT NULL,
    #                               resolution VARCHAR(64) NOT NULL,
    #                               imei VARCHAR(64) NOT NULL,
    #                               mac VARCHAR(64) NOT NULL,
    #                               is_prison_break INTEGER(2) NOT NULL,
    #                               is_crack INTEGER(2) NOT NULL,
    #                               languages VARCHAR(64) NOT NULL,
    #                               timezone VARCHAR(64) NOT NULL
    #                               );
    #                               ''')


    @gen.coroutine
    def do_async_db2(self, app_id):
        cur = self.application.db.cursor()
        # yield cur.execute(
        #         "SELECT * FROM ten_logservice.t_app WHERE app_id = '%d'" % (app_id))
        # print(cur.description)
        # if cur.rowcount > 0:
        #     app_id = cur.lastrowid
        if app_id == '':
            return
        # 创建应用所需表
        import tornado_mysql
        try:
            yield cur.execute('SELECT * FROM t_device_' + str(app_id))
            print(cur.description)
        except tornado_mysql.ProgrammingError:
            pass
            # --------------------------------------------------------------------------------
            # 设备表
            try:
                yield cur.execute('''
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
                yield cur.execute('''
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
                yield cur.execute('''
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
            # # 事件属性表
            # try:
            #     yield cur.execute('''
            #               DROP TABLE IF EXISTS t_user_event_attr_''' + str(app_id) + ''';
            #               CREATE TABLE t_user_event_attr_''' + str(app_id) + ''' (
            #               ls_id INTEGER(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            #               device_id INTEGER(4) NOT NULL,
            #               user_id INTEGER(4) NOT NULL,
            #               session_id INTEGER(8) NOT NULL,
            #               event_id INTEGER(4) NOT NULL,
            #               event_name VARCHAR(128) NOT NULL,
            #               attr_id INTEGER(4) NOT NULL,
            #               attr_name VARCHAR(64) NOT NULL,
            #               attr_data_type VARCHAR(64) NOT NULL,
            #               attr_value VARCHAR(128) NOT NULL,
            #               begin_date TIMESTAMP NOT NULL,
            #               begin_day_id INTEGER(4) NOT NULL,
            #               platform INTEGER(2) NOT NULL,
            #               utc_date_s VARCHAR(16) NOT NULL
            #               );
            #               ''')
            # except:
            #     pass
            # --------------------------------------------------------------------------------
            # 事件总表
            try:
            # if True:
                yield cur.execute('''
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
        # yield cur.execute("DROP TABLE IF EXISTS '%s';"
        #                   "CREATE TABLE '%s' ("
        #                   "device_id INTEGER(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        #                   "device_md5 VARCHAR(128) NOT NULL,"
        #                   "platform INTEGER(2) NOT NULL UNIQUE,"
        #                   "device_type VARCHAR(64) NOT NULL,"
        #                   "l INTEGER(4) NOT NULL,"
        #                   "h INTEGER(4) NOT NULL,"
        #                   "device_brand VARCHAR(64) NOT NULL,"
        #                   "device_model VARCHAR(64) NOT NULL,"
        #                   "resolution VARCHAR(64) NOT NULL,"
        #                   "imei VARCHAR(64) NOT NULL,"
        #                   "mac VARCHAR(64) NOT NULL,"
        #                   "is_prison_break INTEGER(2) NOT NULL,"
        #                   "is_crack INTEGER(2) NOT NULL,"
        #                   "languages VARCHAR(64) NOT NULL,"
        #                   "timezone VARCHAR(64) NOT NULL"
        #                   ");"
        #                   % ('t_device_' + str(app_id),
        #                      't_device_' + str(app_id)))
        cur.close()
        raise gen.Return((200, {}))



class IdentifyServiceHandler(BaseHandler):
    @gen.coroutine
    def handler(self):
        # 获取请求参数
        app_key = self.get_argument("app_key")
        # device_id = self.get_argument("device_id")

        # 设备信息
        device_info = self.get_argument("device_info")
        # device_md5 = self.get_argument("device_md5")
        # device_type = self.get_argument("device_type")
        # l = self.get_argument("l")
        # h = self.get_argument("h")
        # device_brand = self.get_argument("device_brand")
        # device_model = self.get_argument("device_model")
        # resolution = self.get_argument("resolution")
        # imei = self.get_argument("imei")
        # mac = self.get_argument("mac")
        # is_prison_break = self.get_argument("is_prison_break")
        # is_crack = self.get_argument("is_crack")
        # languages = self.get_argument("language")
        # timezone = self.get_argument("timezone")


        user_id = self.get_argument("user_id")
        # ls_id = self.get_argument("ls_id")
        # begin_date = self.get_argument("begin_date")
        platform = int(self.get_argument("platform"))
        user_property = self.get_argument("user_property")  # json类型

        # 异步数据库操作
        app_id = yield self.do_async_db(app_key)
        # 1002:  应用不存在
        if app_id == '':
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("Identify", 1002, '您还没有注册此应用', {})
            return self.finish(rsp)

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
        # 手机设备id
        (status, device_id) = yield self.do_async_db2(app_id, device_md5, platform, device_type, l, h, device_brand,
                                                      device_model,
                                                      resolution, imei, mac, is_prison_break, is_crack, languages,
                                                      timezone, user_id, timestamp)

        if status == 0:
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("Identify", 1003, '您已经有该设备信息了', {})
            return self.finish(rsp)

        # begin_date = time.time()

        (status, ls_id) = yield self.do_async_db3(app_id, user_id, device_id, begin_date, platform)

        property_object = json.loads(user_property)
        for p in property_object.keys():
            print(p, property_object[p], type(p), type(property_object[p]))
            property_name = p
            property_data_type = str(type(property_object[p])).replace('<class \'', '').replace('\'>', '')
            property_value = str(property_object[p])
            property_id = yield self.do_async_db4(app_id, user_id, ls_id, property_name, property_data_type,
                                                  property_value, platform)

        print("success")

        # self.application.db.rollback()
        self.application.db.commit()


    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def get(self):
        yield self.handler()
        self.set_header('content-type', 'application/json')
        rsp = self.set_res_data("track", 200, "success", {})
        return self.finish(rsp)


    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def post(self):
        yield self.handler()
        self.set_header('content-type', 'application/json')
        rsp = self.set_res_data("track", 200, "success", {})
        return self.finish(rsp)

        # yield self.handler()
        # self.set_header('content-type', 'application/json')
        # rsp = self.set_res_data("track", 200, "success", {})
        # return self.finish(rsp)
        #
        # # 获取请求参数
        # app_key = self.get_argument("app_key")
        # # device_id = self.get_argument("device_id")
        #
        # # 设备信息
        # device_info = self.get_argument("device_info")
        # # device_md5 = self.get_argument("device_md5")
        # # device_type = self.get_argument("device_type")
        # # l = self.get_argument("l")
        # # h = self.get_argument("h")
        # # device_brand = self.get_argument("device_brand")
        # # device_model = self.get_argument("device_model")
        # # resolution = self.get_argument("resolution")
        # # imei = self.get_argument("imei")
        # # mac = self.get_argument("mac")
        # # is_prison_break = self.get_argument("is_prison_break")
        # # is_crack = self.get_argument("is_crack")
        # # languages = self.get_argument("language")
        # # timezone = self.get_argument("timezone")
        #
        #
        # user_id = self.get_argument("user_id")
        # # ls_id = self.get_argument("ls_id")
        # # begin_date = self.get_argument("begin_date")
        # platform = int(self.get_argument("platform"))
        # user_property = self.get_argument("user_property") #json类型
        #
        # # 异步数据库操作
        # app_id = yield self.do_async_db(app_key)
        # # 1002:  应用不存在
        # if app_id == '':
        #     # 处理返回值、返回数据
        #     self.set_header('content-type', 'application/json')
        #     rsp = self.set_res_data("Identify", 1002, '您还没有注册此应用', {})
        #     return self.finish(rsp)
        #
        # # 设备信息
        # device_info_object = json.loads(device_info)
        # # for di in device_info_object.keys():
        # device_md5 = device_info_object["device_md5"]
        # # platform = device_info_object["platform"]
        # device_type = device_info_object["device_type"]
        # l = device_info_object["l"]
        # h = device_info_object["h"]
        # device_brand = device_info_object["device_brand"]
        # device_model = device_info_object["device_model"]
        # resolution = device_info_object["resolution"]
        # imei = device_info_object["imei"]
        # mac = device_info_object["mac"]
        # is_prison_break = device_info_object["is_prison_break"]
        # is_crack = device_info_object["is_crack"]
        # languages = device_info_object["language"]
        # timezone = device_info_object["timezone"]
        #
        # # 手机设备id
        # (status, device_id) = yield self.do_async_db2(app_id, device_md5, platform, device_type, l, h, device_brand, device_model,
        #                                     resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id)
        #
        # if status == 0:
        #     # 处理返回值、返回数据
        #     self.set_header('content-type', 'application/json')
        #     rsp = self.set_res_data("Identify", 1003, '您已经有该设备信息了', {})
        #     return self.finish(rsp)
        #
        # # begin_date = time.time()
        # begin_date = datetime.datetime.now()
        # begin_date = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        # (status, ls_id) = yield self.do_async_db3(app_id, user_id, device_id, begin_date, platform)
        #
        # property_object = json.loads(user_property)
        # for p in property_object.keys():
        #     print(p, property_object[p], type(p), type(property_object[p]))
        #     property_name = p
        #     property_data_type = str(type(property_object[p])).replace('<class \'', '').replace('\'>', '')
        #     property_value = str(property_object[p])
        #     property_id = yield self.do_async_db4(app_id, user_id, ls_id, property_name, property_data_type, property_value, platform)
        #
        #
        # print("success")
        #
        #
        #
        #
        # # self.application.db.rollback()
        # self.application.db.commit()
        #
        #
        #
        #
        # # 处理返回值、返回数据
        # self.set_header('content-type', 'application/json')
        # ret = {
        #     "ls_id": ls_id
        # }
        # rsp = self.set_res_data("Identify", 200, 'success', ret)
        # return self.finish(rsp)

    @gen.coroutine
    def do_async_db(self, app_key):
        cur = self.application.db.cursor()
        yield cur.execute("SELECT * FROM ten_logservice.t_app WHERE app_key = '%s'" % app_key)
        if cur.rowcount > 0:
            app_id = cur.fetchone()[0]

            raise gen.Return(app_id)
        else:
            raise gen.Return('')

    @gen.coroutine
    def do_async_db2(self, app_id, device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id, timestamp):
        types = 1
        device_id = 0
        cur = self.application.db.cursor()
        try:
            yield cur.execute(
                "INSERT INTO ten_logservice.t_device_" + str(
                    app_id) + " (device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id, types, timestamp) VALUES"
                              " ('%s', '%d', '%s', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%s', '%s', '%d', '%s')" % (
                                 device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id, types, timestamp))

            if cur.rowcount > 0:
                device_id = cur.lastrowid

        except:
            print('写入数据库失败')
            # 回滚
            # yield self.application.db.rollback()
            ret = {'msg': '创建失败', 'data': {}}
            raise gen.Return((0, device_id))

        yield cur.close()

        # self.application.db.commit()

        print(device_id)

        raise gen.Return((1, device_id))

    @gen.coroutine
    def do_async_db3(self, app_id, user_id, device_id, begin_date, platform):
        # begin_date = int(begin_date)
        cur = self.application.db.cursor()

        yield cur.execute(
            "SELECT * FROM ten_logservice.t_user_" + str(
                app_id) + " WHERE user_id = '%s'" % (user_id)
        )

        if cur.rowcount > 0:
            ls_id = cur.fetchone()[0]
            yield cur.execute("UPDATE ten_logservice.t_user_" + str(app_id) + " "
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
                yield cur.execute(
                    "INSERT INTO ten_logservice.t_user_" + str(app_id) + " (user_id, device_id, begin_date, platform) VALUES ('%s', '%d', '%s', '%d')" % (user_id, device_id, begin_date, platform))

                if cur.rowcount > 0:
                    ls_id = cur.lastrowid

            except:

                print('写入数据库失败')
                # 回滚
                # yield self.application.db.rollback()
                ret = {'msg': '创建失败', 'data': {}}
                raise gen.Return((1001, ls_id))

        yield cur.close()


        print(ls_id)

        raise gen.Return((200, ls_id))

    @gen.coroutine
    def do_async_db4(self, app_id, user_id, ls_id, property_name, property_data_type, property_value, platform):
        cur = self.application.db.cursor()

        yield cur.execute("SELECT * FROM ten_logservice.t_user_property_" + str(app_id) +
                          " WHERE ls_id = '%d' AND property_name = '%s' AND user_id = '%s'" %
                          (ls_id, property_name, user_id)
                          )

        if cur.rowcount > 0:
            property_id = cur.fetchone()[0]
            yield cur.execute("UPDATE ten_logservice.t_user_property_" + str(app_id) +
                              " SET property_name = '%s', property_data_type = '%s', property_value = '%s', platform = '%d' WHERE property_id = '%d' " % (
                                  property_name, property_data_type, property_value, platform, property_id)
                              )
        else:

            try:
            # if True:
                yield cur.execute(
                    "INSERT INTO ten_logservice.t_user_property_" + str(
                        app_id) + " (user_id, ls_id, property_name, property_data_type, property_value, platform) VALUES "
                                  "('%s', '%d', '%s', '%s', '%s', '%d')" % (
                                     user_id, ls_id, property_name, property_data_type, property_value, platform))

                if cur.rowcount > 0:
                    property_id = cur.lastrowid

            except:
                print('写入数据库失败')
                # 回滚
                # yield self.application.db.rollback()
                ret = {'msg': '创建失败', 'data': {}}
                raise gen.Return((1001, ret))

        yield cur.close()

        # print(property_id)

        raise gen.Return((1001, {}))







class TrackServcieHandler(BaseHandler):
    @gen.coroutine
    def handler(self):
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
        app_id = yield self.do_async_db(app_key)
        if app_id == '':
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("Identify", 1002, '您还没有注册此应用', {})
            return self.finish(rsp)

        begin_date = datetime.datetime.now()
        begin_date = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = begin_date
        # 手机设备id
        device_id = yield self.do_async_db2(app_id, device_md5, platform, device_type, l, h, device_brand, device_model,
                                            resolution, imei, mac, is_prison_break, is_crack, languages, timezone,
                                            user_id, timestamp)


        utc_date_s = begin_date
        session_id = 1
        begin_day_id = 1
        ls_id = 1

        (status, event_id) = yield self.do_async_db3(app_id, device_id, user_id, ls_id, session_id, event_name,
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

            yield self.do_async_db4(app_id, event_id, device_id, user_id, ls_id, session_id, event_name, attr_name,
                                    attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s)

        self.application.db.commit()


    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def get(self):
        yield self.handler()
        self.set_header('content-type', 'application/json')
        rsp = self.set_res_data("track", 200, "success", {})
        return self.finish(rsp)


    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def post(self):
        yield self.handler()
        self.set_header('content-type', 'application/json')
        rsp = self.set_res_data("track", 200, "success", {})
        return self.finish(rsp)

        # # 获取请求参数
        # app_key = self.get_argument("app_key")
        #
        # user_id = self.get_argument("user_id")
        #
        # # event_name = self.get_argument("event_name")
        # # event_attr = self.get_argument("event_attr") #json类型
        # #
        # #
        # # session_id = self.get_argument("seesion_id")
        # #
        # # begin_date = self.get_argument("begin_date")
        # # begin_day_id = self.get_argument("begin_day_id")
        # #
        # #
        # # platform = self.get_argument("platform")
        # # network = self.get_argument("network")
        # # mccmnc = self.get_argument("mccmnc")
        # # useragent = self.get_argument("useragent")
        # #
        # # channel = self.get_argument("channel")
        # #
        # # ip = self.get_argument("ip")
        # # country = self.get_argument("country")
        # # area = self.get_argument("area")
        # # city = self.get_argument("city")
        # #
        # # duration = self.get_argument("duration")
        # # utc_date = self.get_argument("utc_date")
        # #
        # #
        # # # 针对js
        # # website = self.get_argument("website")
        # # current_url = self.get_argument("current_url")
        # # referrer_url = self.get_argument("referrer_url")
        # # bs = self.get_argument("bs")
        # # bv = self.get_argument("bv")
        # # utm_source = self.get_argument("utm_source")
        # # utm_medium = self.get_argument("utm_medium")
        # # utm_campaign = self.get_argument("utm_campaign")
        # # utm_content = self.get_argument("utm_content")
        # # utm_term = self.get_argument("utm_term")
        # #
        # #
        # #
        # # # 针对Android、IOS
        # # app_version = self.get_argument("app_version")
        # # os = self.get_argument("os")
        # # ov = self.get_argument("ov")
        #
        #
        # # 设备信息
        # event_info = self.get_argument("event_info")
        #
        # # 设备信息
        # device_info = self.get_argument("device_info")
        # # 设备信息
        # device_info_object = json.loads(device_info)
        # # for di in device_info_object.keys():
        # device_md5 = device_info_object["device_md5"]
        # # platform = device_info_object["platform"]
        # device_type = device_info_object["device_type"]
        # l = device_info_object["l"]
        # h = device_info_object["h"]
        # device_brand = device_info_object["device_brand"]
        # device_model = device_info_object["device_model"]
        # resolution = device_info_object["resolution"]
        # imei = device_info_object["imei"]
        # mac = device_info_object["mac"]
        # is_prison_break = device_info_object["is_prison_break"]
        # is_crack = device_info_object["is_crack"]
        # languages = device_info_object["language"]
        # timezone = device_info_object["timezone"]
        #
        #
        # # 事件属性
        # event_attr = self.get_argument("event_attr")
        #
        # platform = int(self.get_argument("platform"))
        #
        #
        # event_info = json.loads(event_info)
        #
        # # 共有的事件属性
        # event_name = event_info["event_name"]
        # network = int(event_info["network"])
        # mccmnc = event_info["mccmnc"] # 运营商
        # useragent = event_info["useragent"]
        # channel = event_info["channel"]
        # ip = str(event_info["ip"])
        # duration = event_info["duration"]
        # utc_date = event_info["utc_date"]
        #
        # country = ''
        # area = ''
        # city = ''
        #
        # region = ''
        #
        # ip_json = {"ip": ip}
        # # ip_json = json.dump(ip_json)
        # (country, area, region, city, mccmnc) = IP.checkip(ip=ip_json)
        #
        # # if mccmnc ==
        #
        #
        # # --------------------------
        # app_version = ''
        # os = ''
        # ov = 0
        #
        # website = ''
        # current_url = ''
        # referrer_url = ''
        # bs = ''
        # bv = 0
        # utm_source = ''
        # utm_medium = ''
        # utm_campaign = ''
        # utm_content = ''
        # utm_term = ''
        #
        # if platform == 1 or platform == 2: # Android or IOS
        #     app_version = event_info["app_version"]
        #     os = event_info["os"]
        #     ov = event_info["ov"]
        #
        #
        # elif platform == 3: # JS
        #     website = event_info["website"]
        #     current_url = event_info["current_url"]
        #     referrer_url = event_info["referrer_url"]
        #     bs = event_info["bs"]
        #     bv = event_info["bv"]
        #     utm_source = event_info["utm_source"]
        #     utm_medium = event_info["utm_medium"]
        #     utm_campaign = event_info["utm_campaign"]
        #     utm_content = event_info["utm_content"]
        #     utm_term = event_info["utm_term"]
        #
        #
        #
        # # 异步数据库操作
        # app_id = yield self.do_async_db(app_key)
        # if app_id == '':
        #     # 处理返回值、返回数据
        #     self.set_header('content-type', 'application/json')
        #     rsp = self.set_res_data("Identify", 1002, '您还没有注册此应用', {})
        #     return self.finish(rsp)
        #
        #
        # # 手机设备id
        # device_id = yield self.do_async_db2(app_id, device_md5, platform, device_type, l, h, device_brand, device_model,
        #                                     resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id)
        #
        # begin_date = datetime.datetime.now()
        # begin_date = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        # utc_date_s = begin_date
        # session_id = 1
        # begin_day_id = 1
        # ls_id = 1
        #
        # (status, event_id) = yield self.do_async_db3(app_id, device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network, mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area, city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration, utc_date_s)
        # # if status == 0:
        # #     # 处理返回值、返回数据
        # #     self.set_header('content-type', 'application/json')
        # #     rsp = self.set_res_data("Identify", 1005, '该事件已经注册过了', {})
        # #     return self.finish(rsp)
        #
        #
        #
        # event_attr_object = json.loads(event_attr)
        # for p in event_attr_object.keys():
        #     print(p, event_attr_object[p], type(p), type(event_attr_object[p]))
        #     attr_name = p
        #     attr_data_type = str(type(event_attr_object[p])).replace('<class \'', '').replace('\'>', '')
        #     attr_value = str(event_attr_object[p])
        #
        #     yield self.do_async_db4(app_id, event_id, device_id, user_id, ls_id, session_id, event_name, attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s)
        #
        #
        #
        #
        # self.application.db.commit()
        #
        # # self.application.db.rollback()
        #
        #
        # # 处理返回值、返回数据
        # self.set_header('content-type', 'application/json')
        # rsp = self.set_res_data("track", 200, "success", {})
        # # return rsp
        # return self.finish(rsp)
        # # self.write(rsp)


    @gen.coroutine
    def do_async_db(self, app_key):
        app_id = 0
        cur = self.application.db.cursor()
        try:
            yield cur.execute("SELECT * FROM ten_logservice.t_app WHERE app_key = '%s'" % app_key)
            if cur.rowcount > 0:
                app_id = cur.fetchone()[0]

                raise gen.Return(app_id)
            else:
                raise gen.Return('')
        except:
            pass
            raise gen.Return(app_id)


    @gen.coroutine
    def do_async_db2(self, app_id, device_md5, platform, device_type, l, h, device_brand, device_model, resolution,
                     imei, mac, is_prison_break, is_crack, languages, timezone, user_id, timestamp):
        types = 2
        device_id = 0
        cur = self.application.db.cursor()
        # try:
        if True:
            yield cur.execute(
                "INSERT INTO ten_logservice.t_device_" + str(
                    app_id) + " (device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id, types, timestamp) VALUES"
                              " ('%s', '%d', '%s', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%s', '%s', '%d', '%s')" % (
                    device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac,
                    is_prison_break, is_crack, languages, timezone, user_id, types, timestamp))

            if cur.rowcount > 0:
                device_id = cur.lastrowid

        # except:
        #     print('写入数据库失败')
        #     # 回滚
        #     # yield self.application.db.rollback()
        #     ret = {'msg': '创建失败', 'data': {}}
        #     raise gen.Return(device_id)

        yield cur.close()

        # self.application.db.commit()

        print(device_id)

        raise gen.Return(device_id)

    @gen.coroutine
    def do_async_db3(self, app_id, device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network, mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area, city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration, utc_date_s):
        event_id = 0
        # user_id = int(user_id)
        cur = self.application.db.cursor()

        yield cur.execute("SELECT * FROM ten_logservice.t_event_all_" + str(app_id) +
                          " WHERE ls_id = '%d' AND event_name = '%s' AND user_id = '%s'" %
                          (ls_id, event_name, user_id)
                          )

        if cur.rowcount > 0:
            event_id = cur.fetchone()[0]

            yield cur.execute("UPDATE ten_logservice.t_event_all_" + str(app_id) + " "
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

            try:
                yield cur.execute(
                    "INSERT INTO ten_logservice.t_event_all_" + str(
                        app_id) + " (device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network, mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area, city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration, utc_date_s) VALUES"
                                  " ('%d',      '%s',    '%d',  '%d',       '%s',       '%s',       '%d',         '%d',     '%d',    '%s',   '%s',      '%s',    '%s',        '%s',         '%s',    '%s',       '%s', '%s',  '%s', '%s','%s','%d','%s','%d', '%s',    '%s',       '%s',         '%s',        '%s',     '%d',     '%s')" % (
                                     device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network, mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area, city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration, utc_date_s))

                if cur.rowcount > 0:
                    event_id = cur.lastrowid

            except:



                # yield cur.execute(
                #     "SELECT * FROM ten_logservice.t_event_all_" + str(app_id) + " WHERE event_name = '%s' AND user_id = '%s'" % (event_name, user_id)
                # )
                #
                # if cur.rowcount > 0:
                #     event_id = cur.fetchone()[0]

                print('写入数据库失败')
                # 回滚
                # yield self.application.db.rollback()
                ret = {'msg': '创建失败', 'data': {}}
                raise gen.Return((0, session_id))

        yield cur.close()

        # self.application.db.commit()

        print(event_id)

        raise gen.Return((1, event_id))

    @gen.coroutine
    def do_async_db4(self, app_id, event_id, device_id, user_id, ls_id, session_id, event_name, attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s):
        user_id = int(user_id)
        cur = self.application.db.cursor()
        try:
            yield cur.execute('SELECT * FROM t_user_event_attr_' + str(app_id) + '_' + str(event_id))
            print(cur.description)
        except tornado_mysql.ProgrammingError:
            print('新建事件属性表...')
            # 事件属性表
            try:
                yield cur.execute('''
                              DROP TABLE IF EXISTS t_user_event_attr_''' + str(app_id) + '''_''' + str(event_id) + ''';
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



        yield cur.execute("SELECT * FROM ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) +
                          " WHERE event_name = '%s' AND attr_name = '%s' AND user_id = '%s'" %
                          (event_name, attr_name, user_id)
                          )

        if cur.rowcount > 0:

            attr_id = cur.fetchone()[0]

            yield cur.execute("UPDATE ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) +
                              " SET attr_name = '%s', attr_data_type = '%s', attr_value = '%s', begin_date = '%s', begin_day_id = '%d', platform = '%d', utc_date_s = '%s' WHERE attr_id = '%d' " % (
                              attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s, attr_id)
                              )

        else:

            try:
            # if True:
                yield cur.execute(
                    "INSERT INTO ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) + \
                    " (device_id, user_id, ls_id, session_id, event_id, event_name, attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s) VALUES"
                    " ('%d',      '%s',    '%d',  '%d',       '%s',     '%s',       '%s',      '%s',           '%s',       '%s',       '%d',         '%d',     '%s')" % (
                       device_id, user_id, ls_id, session_id, event_id, event_name, attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s))

                if cur.rowcount > 0:
                    session_id = cur.lastrowid

            except:
                print('写入数据库失败')
                # 回滚
                # yield self.application.db.rollback()
                ret = {'msg': '创建失败', 'data': {}}
                raise gen.Return((0, session_id))


        cur.close()
        raise gen.Return((200, {}))



class StartTrackServcieHandler(BaseHandler):
    @gen.coroutine
    def handler(self):
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
        app_id = yield self.do_async_db(app_key)
        if app_id == '':
            # 处理返回值、返回数据
            self.set_header('content-type', 'application/json')
            rsp = self.set_res_data("Identify", 1002, '您还没有注册此应用', {})
            return self.finish(rsp)

        begin_date = datetime.datetime.now()
        begin_date = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = begin_date
        # 手机设备id
        device_id = yield self.do_async_db2(app_id, device_md5, platform, device_type, l, h, device_brand, device_model,
                                            resolution, imei, mac, is_prison_break, is_crack, languages, timezone,
                                            user_id, timestamp)


        utc_date_s = begin_date
        session_id = 1
        begin_day_id = 1
        ls_id = 1

        (status, event_id) = yield self.do_async_db3(app_id, device_id, user_id, ls_id, session_id, event_name,
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

            yield self.do_async_db4(app_id, event_id, device_id, user_id, ls_id, session_id, event_name, attr_name,
                                    attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s)

        self.application.db.commit()

    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def get(self):
        yield self.handler()
        self.set_header('content-type', 'application/json')
        rsp = self.set_res_data("track", 200, "success", {})
        return self.finish(rsp)

    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def post(self):
        yield self.handler()
        self.set_header('content-type', 'application/json')
        rsp = self.set_res_data("track", 200, "success", {})
        return self.finish(rsp)

    @gen.coroutine
    def do_async_db(self, app_key):
        app_id = 0
        cur = self.application.db.cursor()
        try:
            yield cur.execute("SELECT * FROM ten_logservice.t_app WHERE app_key = '%s'" % app_key)
            if cur.rowcount > 0:
                app_id = cur.fetchone()[0]

                raise gen.Return(app_id)
            else:
                raise gen.Return('')
        except:
            pass
            raise gen.Return(app_id)

    @gen.coroutine
    def do_async_db2(self, app_id, device_md5, platform, device_type, l, h, device_brand, device_model, resolution,
                     imei, mac, is_prison_break, is_crack, languages, timezone, user_id, timestamp):
        types = 2
        device_id = 0
        cur = self.application.db.cursor()
        # try:
        if True:
            yield cur.execute(
                "INSERT INTO ten_logservice.t_device_" + str(
                    app_id) + " (device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac, is_prison_break, is_crack, languages, timezone, user_id, types, timestamp) VALUES"
                              " ('%s', '%d', '%s', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%s', '%s', '%d', '%s')" % (
                    device_md5, platform, device_type, l, h, device_brand, device_model, resolution, imei, mac,
                    is_prison_break, is_crack, languages, timezone, user_id, types, timestamp))

            if cur.rowcount > 0:
                device_id = cur.lastrowid

        # except:
        #     print('写入数据库失败')
        #     # 回滚
        #     # yield self.application.db.rollback()
        #     ret = {'msg': '创建失败', 'data': {}}
        #     raise gen.Return(device_id)

        yield cur.close()

        # self.application.db.commit()

        print(device_id)

        raise gen.Return(device_id)

    @gen.coroutine
    def do_async_db3(self, app_id, device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id,
                     platform, network, mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip,
                     country, area, city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term,
                     duration, utc_date_s):
        event_id = 0
        # user_id = int(user_id)
        cur = self.application.db.cursor()

        yield cur.execute("SELECT * FROM ten_logservice.t_event_all_" + str(app_id) +
                          " WHERE ls_id = '%d' AND event_name = '%s' AND user_id = '%s'" %
                          (ls_id, event_name, user_id)
                          )

        if cur.rowcount > 0:
            event_id = cur.fetchone()[0]

            yield cur.execute("UPDATE ten_logservice.t_event_all_" + str(app_id) + " "
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

            try:
                yield cur.execute(
                    "INSERT INTO ten_logservice.t_event_all_" + str(
                        app_id) + " (device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network, mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area, city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration, utc_date_s) VALUES"
                                  " ('%d',      '%s',    '%d',  '%d',       '%s',       '%s',       '%d',         '%d',     '%d',    '%s',   '%s',      '%s',    '%s',        '%s',         '%s',    '%s',       '%s', '%s',  '%s', '%s','%s','%d','%s','%d', '%s',    '%s',       '%s',         '%s',        '%s',     '%d',     '%s')" % (
                        device_id, user_id, ls_id, session_id, event_name, begin_date, begin_day_id, platform, network,
                        mccmnc, useragent, website, current_url, referrer_url, channel, app_version, ip, country, area,
                        city, os, ov, bs, bv, utm_source, utm_medium, utm_campaign, utm_content, utm_term, duration,
                        utc_date_s))

                if cur.rowcount > 0:
                    event_id = cur.lastrowid

            except:

                # yield cur.execute(
                #     "SELECT * FROM ten_logservice.t_event_all_" + str(app_id) + " WHERE event_name = '%s' AND user_id = '%s'" % (event_name, user_id)
                # )
                #
                # if cur.rowcount > 0:
                #     event_id = cur.fetchone()[0]

                print('写入数据库失败')
                # 回滚
                # yield self.application.db.rollback()
                ret = {'msg': '创建失败', 'data': {}}
                raise gen.Return((0, session_id))

        yield cur.close()

        # self.application.db.commit()

        print(event_id)

        raise gen.Return((1, event_id))

    @gen.coroutine
    def do_async_db4(self, app_id, event_id, device_id, user_id, ls_id, session_id, event_name, attr_name,
                     attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s):
        user_id = int(user_id)
        cur = self.application.db.cursor()
        try:
            yield cur.execute('SELECT * FROM t_user_event_attr_' + str(app_id) + '_' + str(event_id))
            print(cur.description)
        except tornado_mysql.ProgrammingError:
            print('新建事件属性表...')
            # 事件属性表
            try:
                yield cur.execute('''
                                  DROP TABLE IF EXISTS t_user_event_attr_''' + str(app_id) + '''_''' + str(event_id) + ''';
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

        yield cur.execute("SELECT * FROM ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) +
                          " WHERE event_name = '%s' AND attr_name = '%s' AND user_id = '%s'" %
                          (event_name, attr_name, user_id)
                          )

        if cur.rowcount > 0:

            attr_id = cur.fetchone()[0]

            yield cur.execute("UPDATE ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) +
                              " SET attr_name = '%s', attr_data_type = '%s', attr_value = '%s', begin_date = '%s', begin_day_id = '%d', platform = '%d', utc_date_s = '%s' WHERE attr_id = '%d' " % (
                                  attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s,
                                  attr_id)
                              )

        else:

            try:
                # if True:
                yield cur.execute(
                    "INSERT INTO ten_logservice.t_user_event_attr_" + str(app_id) + "_" + str(event_id) + \
                    " (device_id, user_id, ls_id, session_id, event_id, event_name, attr_name, attr_data_type, attr_value, begin_date, begin_day_id, platform, utc_date_s) VALUES"
                    " ('%d',      '%s',    '%d',  '%d',       '%s',     '%s',       '%s',      '%s',           '%s',       '%s',       '%d',         '%d',     '%s')" % (
                        device_id, user_id, ls_id, session_id, event_id, event_name, attr_name, attr_data_type,
                        attr_value, begin_date, begin_day_id, platform, utc_date_s))

                if cur.rowcount > 0:
                    session_id = cur.lastrowid

            except:
                print('写入数据库失败')
                # 回滚
                # yield self.application.db.rollback()
                ret = {'msg': '创建失败', 'data': {}}
                raise gen.Return((0, session_id))

        cur.close()
        raise gen.Return((200, {}))


class EndTrackServcieHandler(BaseHandler):
    @gen.coroutine
    def handler(self):
        # 获取请求参数
        app_key = self.get_argument("app_key")
        user_id = self.get_argument("user_id")
        event_name = self.get_argument("event_name")
        # app_key = self.get_argument("app_key")
        #
        # user_id = self.get_argument("user_id")
        #
        # # 设备信息
        # event_info = self.get_argument("event_info")
        #
        # # 设备信息
        # device_info = self.get_argument("device_info")
        # # 设备信息
        # device_info_object = json.loads(device_info)
        # # for di in device_info_object.keys():
        # device_md5 = device_info_object["device_md5"]
        # # platform = device_info_object["platform"]
        # device_type = device_info_object["device_type"]
        # l = device_info_object["l"]
        # h = device_info_object["h"]
        # device_brand = device_info_object["device_brand"]
        # device_model = device_info_object["device_model"]
        # resolution = device_info_object["resolution"]
        # imei = device_info_object["imei"]
        # mac = device_info_object["mac"]
        # is_prison_break = device_info_object["is_prison_break"]
        # is_crack = device_info_object["is_crack"]
        # languages = device_info_object["language"]
        # timezone = device_info_object["timezone"]
        #
        # # 事件属性
        # event_attr = self.get_argument("event_attr")
        #
        # platform = int(self.get_argument("platform"))
        #
        # event_info = json.loads(event_info)
        #
        # # 共有的事件属性
        # event_name = event_info["event_name"]
        # network = int(event_info["network"])
        # mccmnc = event_info["mccmnc"]  # 运营商
        # useragent = event_info["useragent"]
        # channel = event_info["channel"]
        # ip = str(event_info["ip"])
        # # duration = event_info["duration"]
        # utc_date = event_info["utc_date"]
        #
        # country = ''
        # area = ''
        # city = ''
        #
        # region = ''
        #
        # ip_json = {"ip": ip}
        # # ip_json = json.dump(ip_json)
        # (country, area, region, city, mccmnc) = IP.checkip(ip=ip_json)
        #
        # # if mccmnc ==
        #
        #
        # # --------------------------
        # app_version = ''
        # os = ''
        # ov = 0
        #
        # website = ''
        # current_url = ''
        # referrer_url = ''
        # bs = ''
        # bv = 0
        # utm_source = ''
        # utm_medium = ''
        # utm_campaign = ''
        # utm_content = ''
        # utm_term = ''
        #
        # if platform == 1 or platform == 2:  # Android or IOS
        #     app_version = event_info["app_version"]
        #     os = event_info["os"]
        #     ov = event_info["ov"]
        #
        #
        # elif platform == 3:  # JS
        #     website = event_info["website"]
        #     current_url = event_info["current_url"]
        #     referrer_url = event_info["referrer_url"]
        #     bs = event_info["bs"]
        #     bv = event_info["bv"]
        #     utm_source = event_info["utm_source"]
        #     utm_medium = event_info["utm_medium"]
        #     utm_campaign = event_info["utm_campaign"]
        #     utm_content = event_info["utm_content"]
        #     utm_term = event_info["utm_term"]

        # 异步数据库操作

        cur = self.application.db.cursor()
        app_id = yield self.do_async_db(cur, app_key)
        # cur.close()

        if app_id == 0:
            # 处理返回值、返回数据

            # self.set_header('content-type', 'application/json')
            # rsp = self.set_res_data("Identify", 1002, '您还没有注册此应用', {})
            # return self.finish(rsp)

            raise gen.Return((1002, r"您还没有注册此应用"))

        # cur = self.application.db.cursor()
        (event_id, begin_date) = yield self.do_async_db2(cur, app_id, event_name)
        # cur.close()

        end_date = datetime.datetime.now()
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        time_b = datetime.datetime.strptime(begin_date, "%Y-%m-%d %H:%M:%S")
        time_e = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        duration = (time_e - time_b).seconds

        utc_date_s = str(end_date)

        # cur = self.application.db.cursor()
        (status, event_id) = yield self.do_async_db3(cur, app_id, event_name, duration, begin_date, utc_date_s)
        cur.close()

        self.application.db.commit()

        raise gen.Return((200, r"success"))


    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def get(self):
        yield self.handler()
        self.set_header('content-type', 'application/json')
        rsp = self.set_res_data("track", 200, "success", {})
        return self.finish(rsp)


    @BaseHandler.record_log
    @web.asynchronous
    @gen.coroutine
    def post(self):
        msg = ""
        try:
            (status, msg) = yield self.handler()
        except:
            pass
        self.set_header('content-type', 'application/json')
        rsp = self.set_res_data("track", 200, msg, {})
        self.write(rsp)
        self.finish()


    @gen.coroutine
    def do_async_db(self, cur, app_key):
        app_id = 0

        try:
            yield cur.execute("SELECT * FROM ten_logservice.t_app WHERE app_key = '%s'" % app_key)
            # yield cur.close()
            if cur.rowcount > 0:
                # app_id = cur.fetchone()[0]
                app_id = cur._rows[0][0]

                raise gen.Return(app_id)
                # return app_id
            else:
                raise gen.Return(0)
                # return ''
        except:
            pass
            raise gen.Return(app_id)
            # return app_id

    @gen.coroutine
    def do_async_db2(self, cur, app_id, event_name):
        event_id = 0
        begin_date = ''
        # cur = self.application.db.cursor()
        # try:
        if True:
            yield cur.execute("SELECT * FROM ten_logservice.t_event_all_" + str(app_id) + " WHERE event_name = '%s'" % event_name)
            # yield cur.close()
            if cur.rowcount > 0:
                event_id = cur.fetchone()[0]
                try:
                    begin_date = str(cur._rows[0][6])
                except:
                    begin_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                raise gen.Return((event_id, begin_date))
                # return (event_id, begin_date)
            else:
                raise gen.Return((0, ''))
                # return (0, '')
        # except:
        #     pass
        #     raise gen.Return((event_id, begin_date))


    @gen.coroutine
    def do_async_db3(self, cur, app_id, event_name, duration, begin_date, utc_date_s):
        # cur = self.application.db.cursor()
        yield cur.execute("UPDATE ten_logservice.t_event_all_" + str(app_id) + " "
                                                                               "SET "
                                                                               # "begin_date = '%s', "
                                                                               "duration = '%d', "
                                                                               "utc_date_s = '%s' "
                                                                               "WHERE "
                                                                               "event_name = '%s'" %
                          (duration, utc_date_s, event_name)) #begin_date,
        # yield cur.close()
        raise gen.Return((200, {}))
        # return (200, {})



# from tornado_mysql import pools, cursors
#
# pools.DEBUG = True
#
#
# POOL = pools.Pool(
#     dict(
#         host='47.90.50.20', port=3306, user='root', passwd='123456', db='ten_logservice', #cursorclass = cursors.DictCursor
#         charset = 'utf8',
#     ),
#     max_idle_connections=1,
#     max_recycle_sec=3)


class AppInfoHtmlHandler(BaseHandler):
    # @BaseHandler.record_log
    # @web.asynchronous
    @gen.coroutine
    def get(self):
        user_id = self.get_argument("user_id")

        cur = yield self.application.db_pool.execute("SELECT * FROM t_user as user, t_app as app WHERE app.user_id = '%s'" % user_id)
        if cur.rowcount:
            try:
                app_id = cur._rows[0]['app_id']
                app_name = cur._rows[0]['app_name']
                user_id = cur._rows[0]['user_id']
                user_name = cur._rows[0]['user_name']
            except:
                pass

        cur = yield self.application.db_pool.execute("SELECT * FROM t_user_" + str(app_id) + " as user, t_device_" + str(app_id) + " as device"
                                                                                                         " WHERE"
                                                                                     " device.user_id = user.user_id")
        log = []
        if cur.rowcount:
            print(r'len1=', len(cur._rows))
            print(r'len2=', len(cur._rows[0]))
            for i in range(len(cur._rows)):
                #     # for j in range(len(cur2._rows[i])):
                #     #     print(i, cur2._rows[i][j])
                #
                #     print('\n')
                # print(r'ls_id', cur2._rows[0][0])
                print(cur._rows[i]['timestamp'], cur._rows[i]['device_model'])
                log.append(str(cur._rows[i]['timestamp']) + "," + cur._rows[i]['device_model'])



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
                    appname = app_name,
                    username = user_name,
                    log = log,
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
        sql = "SELECT * FROM t_user_" + str(app_id) + " as user, t_device_" + str(app_id) + " as device WHERE device.user_id = user.user_id"
        try:
            result = yield cur2.execute("SELECT * FROM t_user_" + str(app_id) + " as user, t_device_" + str(app_id) + " as device"
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