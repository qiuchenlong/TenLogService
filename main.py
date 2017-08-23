# -*- coding: utf-8 -*-
'''
Create on 2017年08月14日 14:54

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''


from tornado import httpserver, ioloop, web, gen
import tornado.options

from tornado.options import define, options


from handlers import HANDLERS, TEMPLATE_PATH


import tornado_mysql



# 定义应用程序启动时的一些参数
define("port", default=8081, help="run on the given port", type=int)
define('debug', default=False, help='Set debug mode', type=bool)
define('mysql_host', default='47.90.50.20', help='blog database host')
define('mysql_port', default=3306, help='blog database port')
define('mysql_database', default='ten_logservice', help='blog database name')
define('mysql_user', default='root', help='blog database user')
define('mysql_password', default='123456', help='blog database password')



class TenApplication(tornado.web.Application):
    def __init__(self, debug = False):
        settings = {
            'template_path': TEMPLATE_PATH,
            'xsrf_cookies': False,
            'cookie_secret': 'lcdC20BuS5yHcRLscDOI5vhqh85wqkBBtvvEI0T9xtU=',
            'autoreload': True,
            'debug': debug
        }
        handlers = HANDLERS
        super(TenApplication, self).__init__(handlers, **settings)

        # self.db = yield tornado_mysql.connect(host=options.mysql_host,
        #                                 port=options.mysql_port,
        #                                 db=options.mysql_database,
        #                                 user=options.mysql_user,
        #                                 passwd=options.mysql_password)
        #
        # self.create_tables()


        self.init_db()
        # self.create_tables()

    @gen.coroutine
    def init_db(self):
        self.db = yield tornado_mysql.connect(host=options.mysql_host,
                                              port=options.mysql_port,
                                              db=options.mysql_database,
                                              user=options.mysql_user,
                                              passwd=options.mysql_password,
                                              charset='utf8',
                                              )
        # self.db.autocommit(True)
        cur = self.db.cursor()
        yield self.create_tapp_tables(cur)
        yield self.create_tuser_tables(cur)



    @gen.coroutine
    def create_tapp_tables(self, cur):
        try:
            yield cur.execute('SELECT * FROM t_app')
            print(cur.description)
        except tornado_mysql.ProgrammingError:
            print('新建app表...')
            try:
            # if True:
                yield cur.execute('''
                                DROP TABLE IF EXISTS t_app;
                                CREATE TABLE t_app(
                                  app_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                  app_key VARCHAR(100) NOT NULL,
                                  app_name VARCHAR(128) NOT NULL UNIQUE,
                                  user_id INT NOT NULL
                                );
                ''')
            except:
                pass


        # try:
        #     cur = db.cursor()
        #     yield cur.execute('SELECT count(*) FROM entries')
        # except tornado_mysql.ProgrammingError:
        #     print("error...")
        #     # subprocess.Popen([
        #     #     'alias mysql=/usr/local/mysql/bin/mysql',
        #     #     'mysql --host=127.0.0.1 --databse=ten_logservice --user=root --password=123456',
        #     #     '123456'
        #     # ], shell=True, stdout=subprocess.PIPE)
        #     subprocess.check_call([
        #         'mysql',
        #         '--host=' + options.mysql_host,
        #         # '--port=' + options.mysql_port,
        #         '--db=' + options.mysql_database,
        #         '--user=' + options.mysql_user,
        #         '--passwd=' + options.mysql_password
        #     ], stdin=open(os.path.join(os.path.dirname(__file__), 'schema.sql')))



    @gen.coroutine
    def create_tuser_tables(self, cur):
        try:
            yield cur.execute('SELECT * FROM t_user')
            print(cur.description)
        except tornado_mysql.ProgrammingError:
            print('新建user表...')
            try:
                yield cur.execute('''
                                DROP TABLE IF EXISTS t_user;
                                CREATE TABLE t_user(
                                  user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                  user_name VARCHAR(64) NOT NULL,
                                  user_phone VARCHAR(64) NOT NULL UNIQUE ,
                                  user_email VARCHAR(64) NOT NULL UNIQUE,
                                  user_password VARCHAR(64) NOT NULL
                                );
                ''')
            except:
                pass


def main():
    tornado.options.parse_command_line()
    # application = tornado.web.Application(
    #     handlers=HANDLERS,
    #     template_path=TEMPLATE_PATH,
    #     xsrf_cookies=False,
    #     cookie_secret='lcdC20BuS5yHcRLscDOI5vhqh85wqkBBtvvEI0T9xtU=',
    #     autoreload=True,
    #     debug=True
    # )
    app = TenApplication(debug=options.debug)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    io_loop = ioloop.IOLoop.instance()
    io_loop.start()


if __name__ == '__main__':
    main()
