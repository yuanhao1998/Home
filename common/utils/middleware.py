# -*- coding: utf_8 -*-
# @Create   : 2021/2/24 9:37 上午
# @Author   : yuan hao
"""
在此编写所有中间件
"""


def login_required(request):
    """
    JWT登陆用户鉴权
    """
    import time

    from flask import g

    from models.user import User
    from utils.exception import AuthError, UserError, LoginError
    from utils.public_method import decode_auth_token

    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token_list = auth_header.split(" ")
        if not auth_token_list or auth_token_list[0] != 'JWT' or len(auth_token_list) != 2:
            raise AuthError()
        else:
            auth_token = auth_token_list[1]
            payload = decode_auth_token(auth_token)
            if isinstance(payload, str):
                raise AuthError('无效的JWT Token')
            else:
                if payload['exp'] < time.time():
                    raise LoginError('登陆过期，请重新登陆')
                else:
                    user = User.query.filter(User.id == payload['data']['user_id']).first()
                    if user:
                        g.user = user
                    else:
                        raise UserError()
    else:
        raise AuthError('No JWT Token')


def cross_domain(response, request):
    """
    配置全局跨域
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
