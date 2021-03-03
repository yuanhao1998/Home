# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:13
# @Author   : yuan hao
import sys
from os.path import dirname, abspath

BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, BASE_DIR + '/common')  # 添加common到根路径

redis = None
db = None
csrf = None


def register_extensions(app):  # 注册组件
    from flask_migrate import Migrate, MigrateCommand
    from flask_script import Manager
    from flask_wtf import CSRFProtect
    from redis import Redis

    from utils.public_method import import_class
    from utils.minix_class import SQLAlchemyMinix
    from utils.converters import register_converters

    global db
    db = SQLAlchemyMinix(app)  # mysql,自定义读写分离

    global redis
    redis = Redis(host='175.24.100.78', port=6379, password='yuan123hao', decode_responses=True)  # redis

    register_converters(app)  # 注册自定义路由转换器

    manager = Manager(app)
    Migrate(app, db)
    import_class('models')  # 导入models文件夹
    manager.add_command('db', MigrateCommand)

    global csrf
    csrf = CSRFProtect(app)  # csrf校验


def register_bp(app):  # 注册蓝图
    from app.resources.user import user_bp
    from app.resources import common_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(common_bp)


def register_middleware(app):  # 注册中间件
    from flask import request

    from utils.middleware import cross_domain
    from utils.middleware import login_required

    @app.before_request
    def before_request():
        login_required(request)

    @app.after_request
    def after_request(response):
        cross_domain(response, request)


def create_flask_app(conf):  # 创建flask实例
    from flask import Flask

    app = Flask(__name__)

    from app.settings.config import conf_dict
    from utils.constants import EXTRA_ENV_CONFIG

    app.config.from_object(conf_dict[conf])  # 加载项目配置

    app.config.from_envvar(EXTRA_ENV_CONFIG, silent=True)  # 加载隐私配置、设置静默

    return app


def create_app(conf):
    from app.settings.logging import setup_log

    setup_log(conf)
    app = create_flask_app(conf)
    register_extensions(app)
    register_bp(app)
    return app
