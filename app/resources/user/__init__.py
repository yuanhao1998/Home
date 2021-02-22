# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:54
# @Author   : yuan hao
from json import dumps

from flask import Blueprint
from flask_restful import Api
from flask_restful.utils import PY3

from utils.response_code import RET, error_map

user_bp = Blueprint('user', __name__)  # 实例化蓝图对象

from .passport import *

user_api = Api(user_bp, prefix='/user')  # 实例化api对象
user_api.add_resource(passport.ImgCodeResource, '/image_code/<uuid:image_code>/')
user_api.add_resource(passport.SMSCodeResource, '/sms_code/')
user_api.add_resource(passport.RegisteredResource, '/registered/')
user_api.add_resource(passport.LoginResource, '/login/')
user_api.add_resource(passport.LogoutResource, '/logout/')


@user_api.representation('application/json')
def output_json(data, code, headers=None):

    settings = current_app.config.get('RESTFUL_JSON', {})

    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    if data == 'ok':
        data = {'errno': RET.OK, 'errmsg': error_map[RET.OK]}

    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
