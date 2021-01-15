# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:21
# @Author   : yuan hao

"""
在此编写所有的项目配置文件
"""
import logging


class DevConfig:
    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:yuan123hao@cdb-dcn8l0ek.cd.tencentcdb.com:10172/blog'  # 连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = False  # 是否打印底层执行的SQL

    SQLALCHEMY_BINDS = {
        'master': 'mysql://root:yuan123hao@cdb-dcn8l0ek.cd.tencentcdb.com:10172/blog',
        'slave': 'mysql://root:yuan123hao@cdb-dcn8l0ek.cd.tencentcdb.com:10172/blog'
    }

    # redis配置
    REDIS_HOST = '175.24.100.78'  # ip
    REDIS_PORT = 7000  # 端口
    REDIS_PWD = 'yuan123hao'
    # # 设置主数据库的ip和端口
    # MASTER_NODES = [
    #     {'host': '49.235.248.183', 'port': 7000, 'password': 'yuan123hao'},
    #     {'host': '49.235.248.183', 'port': 7001, 'password': 'yuan123hao'},
    #     {'host': '49.235.248.183', 'port': 7002, 'password': 'yuan123hao'}
    # ]

    LOG_LEVEL = logging.ERROR  # 日志等级

    SECRET_KEY = 'g_*@^)u-3ll9sqw5-power%fh&_2ev+2@f3z)y=iyo#qi9x+zym_z'  # 密钥

    WTF_CSRF_CHECK_DEFAULT = False  # 全局关闭csrf验证

    # 容联云通讯配置
    R_ACC_ID = '8a216da87249b81301724a854c69010d'
    R_ACC_TOKEN = 'd533e7c5ec87472d90f210c1e799dc7c'
    R_APP_ID = '8a216da87249b81301724a854d740113'

    # 七牛云配置
    QI_ACCESS_KEY = '0qqxuOwqlQbDaQlPpmmdhjswRyLHHXYo2OujZZU7'
    QI_SECRET_KEY = 'PbC1g-VMgM0K3oZ9KEHYBJ_YCUYDSpxXOLVi6SGZ'
    QI_BUCKET_NAME = 'news-yuanhao'
    QI_DOMAIN = 'http://qiniu.waterberry.cn/'


conf_dict = {
    'dev': DevConfig
}
