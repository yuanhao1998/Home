# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:34
# @Author   : yuan hao

"""
在此存放所有重写的类
"""

from flask_sqlalchemy import SignallingSession, SQLAlchemy, get_state
from werkzeug.exceptions import HTTPException

from utils.response_code import error_map


class SessionMinix(SignallingSession):
    def get_bind(self, mapper=None, clause=None):
        """
        重写get_bind方法，配置读写分类
        执行顺序：
            当用户指定数据库，使用用户指定的数据库
            当模型类定义中指定数据库时，使用模型类指定的数据库
            当请求方法为flush、update、delete时，使用主库
            其他操作使用从库
        """

        from sqlalchemy.sql import Update, Delete

        state = get_state(self.app)

        if self._use_bind:
            return state.db.get_engine(self.app, bind=self._use_bind)

        if mapper is not None:
            info = getattr(mapper.mapped_table, 'info', {})
            bind_key = info.get('bind_key')
            if bind_key is not None:
                return state.db.get_engine(self.app, bind=bind_key)

        if self._flushing or isinstance(clause, (Update, Delete)):
            return state.db.get_engine(self.app, bind='master')
        else:
            return state.db.get_engine(self.app, bind='slave')

    _use_bind = None

    def use_bind(self, db=None):
        self._use_bind = db
        return self


class SQLAlchemyMinix(SQLAlchemy):
    def create_session(self, options):
        from sqlalchemy import orm

        return orm.sessionmaker(class_=SessionMinix, db=self, **options)


class APIHTTPException(HTTPException):
    """
    重写HTTPException，配置自定义错误提示信息
    """
    status_code = 4500

    def __init__(self, msg=None):
        super(APIHTTPException, self).__init__()
        self.msg = msg

    @property
    def data(self):
        return {
            'code': self.status_code,
            'msg': self.msg if self.msg else error_map[self.status_code]
        }
