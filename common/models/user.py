# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:58
# @Author   : yuan hao

from datetime import datetime

from sqlalchemy import func, DateTime

from app import db


class BaseModel(db.Model):
    """模型基类，为模型补充创建时间与更新时间"""
    __abstract__ = True

    create_time = db.Column(DateTime, nullable=False, default=func.now())  # 记录的创建时间
    update_time = db.Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())  # 记录的更新时间


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "tb_user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)
