# -*- coding: utf-8 -*-
'''
Create on 2017年08月14日 14:54

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''

import os, sys

import concurrent.futures

import tornado.options
import tornado_mysql
from tornado import gen
from tornado.options import options
from tornado_mysql import pools

from config import config
from controller.base import BaseHandler

from url_mapping import handlers


# # 定义应用程序启动时的一些参数
# define("port", default=8081, help="run on the given port", type=int)
# define('debug', default=False, help='Set debug mode', type=bool)
# define('mysql_host', default='47.90.50.20', help='blog database host')
# define('mysql_port', default=3306, help='blog database port')
# define('mysql_database', default='ten_logservice', help='blog database name')
# define('mysql_user', default='root', help='blog database user')
# define('mysql_password', default='123456', help='blog database password')





# tornado server相关配置
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    compress_response=config['compress_response'],
    xsrf_cookies=config['xsrf_cookies'],
    cookie_secret=config['cookie_secret'],
    login_url=config['login_url'],
    debug=config['debug'],
    default_handler_class=BaseHandler,
)


# tornado_mysql配置及初始化
pools.DEBUG = True
def db_pool_init():
    POOL = pools.Pool(
        dict(
            host = config['database']['host'],
            port = config['database']['port'],
            user = config['database']['user'],
            passwd = config['database']['passwd'],
            db = config['database']['db'],
            charset = config['database']['charset'],
            cursorclass = config['database']['cursorclass'],
        ),
        max_idle_connections = config['database']['max_idle_connections'],
        max_recycle_sec = config['database']['max_recycle_sec'])
    return POOL

def db_table_init(db_pool):
    create_tapp_tables(db_pool)
    create_tuser_tables(db_pool)

@gen.coroutine
def create_tapp_tables(cur):
    try:
        yield cur.execute('SELECT * FROM t_app')
        # print(cur.description)
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
def create_tuser_tables(cur):
    try:
        yield cur.execute('SELECT * FROM t_user')
        # print(cur.description)
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





class TenApplication(tornado.web.Application):
    def __init__(self, debug = False):
        # settings = {
        #     'template_path': TEMPLATE_PATH,
        #     'static_path': STATIC_PATH,
        #     'xsrf_cookies': False,
        #     'cookie_secret': 'lcdC20BuS5yHcRLscDOI5vhqh85wqkBBtvvEI0T9xtU=',
        #     'autoreload': True,
        #     'debug': debug,
        #     # 'default_handler_class': BaseHandlers,
        # }
        # handlers = HANDLERS
        super(TenApplication, self).__init__(handlers, **settings)
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(config['max_threads_num'])
        self.db_pool = db_pool_init()

        db_table_init(self.db_pool)


        # self.db = yield tornado_mysql.connect(host=options.mysql_host,
        #                                 port=options.mysql_port,
        #                                 db=options.mysql_database,
        #                                 user=options.mysql_user,
        #                                 passwd=options.mysql_password)
        #
        # self.create_tables()


        # self.init_db()
        # self.create_tables()



    # @gen.coroutine
    # def init_db(self):
    #     self.db = yield tornado_mysql.connect(host=options.mysql_host,
    #                                           port=options.mysql_port,
    #                                           db=options.mysql_database,
    #                                           user=options.mysql_user,
    #                                           passwd=options.mysql_password,
    #                                           charset='utf8',
    #                                           )
    #     # self.db.autocommit(True)
    #     cur = self.db.cursor()
    #     yield self.create_tapp_tables(cur)
    #     yield self.create_tuser_tables(cur)
    #
    #
    #
    # @gen.coroutine
    # def create_tapp_tables(self, cur):
    #     try:
    #         yield cur.execute('SELECT * FROM t_app')
    #         print(cur.description)
    #     except tornado_mysql.ProgrammingError:
    #         print('新建app表...')
    #         try:
    #         # if True:
    #             yield cur.execute('''
    #                             DROP TABLE IF EXISTS t_app;
    #                             CREATE TABLE t_app(
    #                               app_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #                               app_key VARCHAR(100) NOT NULL,
    #                               app_name VARCHAR(128) NOT NULL UNIQUE,
    #                               user_id INT NOT NULL
    #                             );
    #             ''')
    #         except:
    #             pass
    #
    #
    #     # try:
    #     #     cur = db.cursor()
    #     #     yield cur.execute('SELECT count(*) FROM entries')
    #     # except tornado_mysql.ProgrammingError:
    #     #     print("error...")
    #     #     # subprocess.Popen([
    #     #     #     'alias mysql=/usr/local/mysql/bin/mysql',
    #     #     #     'mysql --host=127.0.0.1 --databse=ten_logservice --user=root --password=123456',
    #     #     #     '123456'
    #     #     # ], shell=True, stdout=subprocess.PIPE)
    #     #     subprocess.check_call([
    #     #         'mysql',
    #     #         '--host=' + options.mysql_host,
    #     #         # '--port=' + options.mysql_port,
    #     #         '--db=' + options.mysql_database,
    #     #         '--user=' + options.mysql_user,
    #     #         '--passwd=' + options.mysql_password
    #     #     ], stdin=open(os.path.join(os.path.dirname(__file__), 'schema.sql')))
    #
    #
    #
    # @gen.coroutine
    # def create_tuser_tables(self, cur):
    #     try:
    #         yield cur.execute('SELECT * FROM t_user')
    #         print(cur.description)
    #     except tornado_mysql.ProgrammingError:
    #         print('新建user表...')
    #         try:
    #             yield cur.execute('''
    #                             DROP TABLE IF EXISTS t_user;
    #                             CREATE TABLE t_user(
    #                               user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #                               user_name VARCHAR(64) NOT NULL,
    #                               user_phone VARCHAR(64) NOT NULL UNIQUE ,
    #                               user_email VARCHAR(64) NOT NULL UNIQUE,
    #                               user_password VARCHAR(64) NOT NULL
    #                             );
    #             ''')
    #         except:
    #             pass


#  从命令行读取配置，如果这些参数不传，默认使用config.py的配置项
def parse_command_line():
    options.define("port", help="run server on a specific port", type=int)
    # options.define("log_console", help="print log to console", type=bool)
    # options.define("log_file", help="print log to file", type=bool)
    # options.define("log_file_path", help="path of log_file", type=str)
    # options.define("log_level", help="level of logging", type=str)
    # # 集群中最好有且仅有一个实例为master，一般用于执行全局的定时任务
    # options.define("master", help="is master node? (true:master / false:slave)", type=bool)
    # # sqlalchemy engine_url, 例如pgsql 'postgresql+psycopg2://mhq:1qaz2wsx@localhost:5432/blog'
    # options.define("engine_url", help="engine_url for sqlalchemy", type=str)
    # # redis相关配置, 覆盖所有用到redis位置的配置
    # options.define("redis_host", help="redis host e.g 127.0.0.1", type=str)
    # options.define("redis_port", help="redis port e.g 6379", type=int)
    # options.define("redis_password", help="redis password set this option if has pwd ", type=str)
    # options.define("redis_db", help="redis db e.g 0", type=int)

    # 读取 项目启动时，命令行上添加的参数项
    options.logging = None  # 不用tornado自带的logging配置
    options.parse_command_line()
    # 覆盖默认的config配置
    if options.port is not None:
        config['port'] = options.port
    # if options.log_console is not None:
    #     config['log_console'] = options.log_console
    # if options.log_file is not None:
    #     config['log_file'] = options.log_file
    # if options.log_file_path is not None:
    #     config['log_file_path'] = options.log_file_path
    # if options.log_level is not None:
    #     config['log_level'] = options.log_level
    # if options.master is not None:
    #     config['master'] = options.master
    # if options.engine_url is not None:
    #     config['database']['engine_url'] = options.engine_url
    # if options.redis_host is not None:
    #     redis_session_config['host'] = options.redis_host
    #     site_cache_config['host'] = options.redis_host
    #     redis_pub_sub_config['host'] = options.redis_host
    # if options.redis_port is not None:
    #     redis_session_config['port'] = options.redis_port
    #     site_cache_config['port'] = options.redis_port
    #     redis_pub_sub_config['port'] = options.redis_port
    # if options.redis_password is not None:
    #     redis_session_config['password'] = options.redis_password
    #     site_cache_config['password'] = options.redis_password
    #     redis_pub_sub_config['password'] = options.redis_password
    # if options.redis_db is not None:
    #     redis_session_config['db_no'] = options.redis_db
    #     site_cache_config['db_no'] = options.redis_db


def main():
    # if len(sys.argv) >= 2:
    #     if sys.argv[1] == 'upgradedb':
    #         # 更新数据库结构，初次获取或更新版本后调用一次python main.py upgradedb即可
    #         from alembic.config import main
    #         main("upgrade head".split(' '), 'alembic')
    #         exit(0)
    # 加载命令行配置
    parse_command_line()
    # # 加载日志管理
    # log_config.init(config['port'], config['log_console'],
    #                 config['log_file'], config['log_file_path'], config['log_level'])
    # 创建application
    application = TenApplication()
    application.listen(config['port'])
    # 全局注册application
    config['application'] = application
    loop = tornado.ioloop.IOLoop.current()
    # # 加载redis消息监听客户端
    # pubsub_manager = PubSubService(redis_pub_sub_config, application, loop)
    # pubsub_manager.long_listen()
    # application.pubsub_manager = pubsub_manager
    # # 为master节点注册定时任务
    # if config['master']:
    #     from extends.time_task import TimeTask
    #     TimeTask(config['database']['engine']).add_cache_flush_task(flush_all_cache).start_tasks()
    loop.start()

    # tornado.options.parse_command_line()
    # # application = tornado.web.Application(
    # #     handlers=HANDLERS,
    # #     template_path=TEMPLATE_PATH,
    # #     xsrf_cookies=False,
    # #     cookie_secret='lcdC20BuS5yHcRLscDOI5vhqh85wqkBBtvvEI0T9xtU=',
    # #     autoreload=True,
    # #     debug=True
    # # )
    # app = TenApplication(debug=options.debug)
    # http_server = httpserver.HTTPServer(app)
    # http_server.listen(options.port)
    # io_loop = ioloop.IOLoop.instance()
    # io_loop.start()


if __name__ == '__main__':
    main()
