# -*- coding: utf_8 -*-
# @Time     : 2020/11/25 11:07
# @Author   : yuan hao
import random
import traceback

from flask import make_response, request, current_app, session
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from app import redis, db
from models.user import User
from utils.captcha.captcha import captcha
from utils.constants import IMG_CODE_EXPIRED_TIME, SMS_CODE_EXPIRED_TIME
from utils.decorators import login_required
from utils.exception import DBError, DataError, DataExistError, ThirdError
from utils.parser import check_mobile_type
from utils.public_method import check_params, send_sms, encode_auth_token
from utils.response_code import RET, error_map


class ImgCodeResource(Resource):

    def get(self, image_code):
        """
        生成图片验证码，存储信息到redis，返回图片，
        :param image_code:前端传递的uuid
        :return: 生成的验证码图片
        """
        name, text, image = captcha.generate_captcha()  # 生成的验证码图片
        redis.setex('img:' + str(image_code), IMG_CODE_EXPIRED_TIME, text)
        response = make_response(image)
        response.headers['Content-Type'] = 'image/jpg'

        return response


class SMSCodeResource(Resource):

    def post(self):
        """
        生成短信验证码，存储信息到redis，发送短信
        :return: 成功或错误信息
        """
        args = request.json
        check_params(args, ['mobile', 'image_code', 'image_code_id'])
        check_mobile_type(args['mobile'])

        try:
            real_code = redis.get('img:' + str(args['image_code_id']))
            if not real_code:
                raise DBError('图片验证码过期')
            if str.lower(real_code) != str.lower(args['image_code']):  # 验证图片验证码是否输入正确
                raise DataError('图片验证码错误')
        except Exception:
            current_app.logger.error(traceback.format_exc())
            raise DBError('请刷新验证码重试')

        redis.delete('img:' + str(args['image_code_id']))  # 验证完成后从redis删除
        user = User.query.filter(User.mobile == args['mobile']).first()  # 校验手机号是否注册
        if user:
            raise DataExistError('该手机号已注册')

        if redis.get('sms:' + str(args['mobile'])):
            raise DBError('您仍可使用之前发送的手机验证码')

        sms_code = '%06d' % random.randint(0, 999999)
        sms_res = send_sms(sms_code, args['mobile'])  # 发送短信
        if sms_res is not None:
            raise ThirdError('发送失败')

        redis.setex('sms:' + args['mobile'], SMS_CODE_EXPIRED_TIME, sms_code)  # 添加短信验证码到redis

        return 'ok'


class RegisteredResource(Resource):

    def post(self):  # 注册实现
        """
        校验参数
        生成密文密码
        添加用户
        设置session
        :return:dict：成功信息
        """
        args = request.json
        check_params(args, ['mobile', 'smscode', 'password'])
        check_mobile_type(args['mobile'])

        real_code = redis.get('sms:' + args['mobile'])
        if not real_code:
            raise DBError('手机号验证码过期')

        if real_code != args['smscode']:
            raise DataError('手机验证码错误')

        # 采用sha256方式，将密码与key混合进行进行加密
        password_hash = generate_password_hash(args['password'] + current_app.config['SECRET_KEY'])
        user = User(mobile=args['mobile'], nick_name=args['mobile'], password_hash=password_hash)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.error(traceback.format_exc())
            raise DBError('注册失败')

        redis.delete('sms:' + args['mobile'])

        token = encode_auth_token(user.id)
        response = make_response({'errno': RET.OK, 'errmsg': error_map[RET.OK]})
        response.headers['Authorization'] = 'JWT ' + token
        return response


class LoginResource(Resource):

    def post(self):  # 登录实现
        """
        校验参数
        从数据库查询数据
        校验密码
        设置session
        :return:dict：成功信息
        """
        args = request.json
        check_params(args, ['mobile', 'password'])
        check_mobile_type(args['mobile'])

        user = User.query.filter(User.mobile == args['mobile']).first()
        if user and check_password_hash(user.password_hash, args['password'] + current_app.config['SECRET_KEY']):
            token = encode_auth_token(user.id)
            response = make_response({'errno': RET.OK, 'errmsg': error_map[RET.OK]})
            response.headers['Authorization'] = 'JWT ' + token
            return response

        raise DataError('登录失败')


class LogoutResource(Resource):

    @login_required
    def post(self):  # 登出实现
        """
        删除浏览器session
        :return: dict：成功信息
        """

        session.pop('id')
        session.pop('name')
        session.pop('mobile')

        return 'ok'
