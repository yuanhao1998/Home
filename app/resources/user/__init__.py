# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:54
# @Author   : yuan hao

from flask import Blueprint
from flask_restful import Api

user_bp = Blueprint('user', __name__)  # 实例化蓝图对象

from .passport import *

user_api = Api(user_bp, prefix='/user')  # 实例化api对象

user_api.add_resource(passport.ImgCodeResource, '/image_code/<uuid:image_code>/')

user_api.add_resource(passport.SMSCodeResource, '/sms_code/')
