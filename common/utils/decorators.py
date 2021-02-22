# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:55
# @Author   : yuan hao

"""
在此编写所有装饰器
"""
from functools import wraps

from flask import session, g

from models.user import User


def check_user(f):  # 检查用户，登录用户获取user，未登录user=None
    @wraps(f)
    def wrapper(*args, **kwargs):

        userid = session.get('id')
        if userid:
            user = User.query.filter(User.id == userid).first()
            g.user = user
        else:
            g.user = None
        return f(*args, **kwargs)

    return wrapper


def login_required(f):  # 登录验证，校验是否登录，未登录抛出异常
    @wraps(f)
    def wrapper(*args, **kwargs):
        from utils.exception import SessionError

        userid = session.get('id')
        if userid:
            user = User.query.filter(User.id == userid).first()
            if user:
                g.user = user
                return f(*args, **kwargs)

        raise SessionError()

    return wrapper


def user_redirect(f):  # 用户重定向，未登录用户重定向到首页
    @wraps(f)
    def wrapper(*args, **kwargs):
        from flask import redirect

        userid = session.get('id')
        if userid:
            user = User.query.get(userid)
            if user:
                g.user = user
                return f(*args, **kwargs)

        return redirect('/')

    return wrapper

