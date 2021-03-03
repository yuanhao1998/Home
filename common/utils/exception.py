# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:55
# @Author   : yuan hao

"""
在此编写所有的自定义异常类型
"""

from utils.minix_class import APIHTTPException
from utils.response_code import RET


class MissParamsError(APIHTTPException):  # 参数缺失
    code = 200
    status_code = RET.PARAMERR


class ParamsTypeError(APIHTTPException):  # 参数格式错误
    code = 200
    status_code = RET.DATAERR


class DBError(APIHTTPException):  # 数据库查询错误
    code = 200
    status_code = RET.DBERR


class NoDataError(APIHTTPException):  # 没有数据
    code = 200
    status_code = RET.NODATA


class DataExistError(APIHTTPException):  # 数据已经存在
    code = 200
    status_code = RET.DATAEXIST


class DataError(APIHTTPException):  # 数据错误
    code = 200
    status_code = RET.DATAERR


class AuthError(APIHTTPException):  # 登陆鉴权失败
    code = 200
    status_code = RET.AUTHERR


class LoginError(APIHTTPException):  # 登录失败
    code = 200
    status_code = RET.LOGINERR


class UserError(APIHTTPException):  # 用户不存在或未激活
    code = 200
    status_code = RET.USERERR


class RoleError(APIHTTPException):  # 用户身份错误
    code = 200
    status_code = RET.ROLEERR


class PasswordError(APIHTTPException):  # 密码错误
    code = 200
    status_code = RET.PWDERR


class RequestError(APIHTTPException):  # 非法请求或请求次数上限
    code = 200
    status_code = RET.REQERR


class IPError(APIHTTPException):  # ip受限
    code = 200
    status_code = RET.IPERR


class ThirdError(APIHTTPException):  # 第三方系统错误
    code = 200
    status_code = RET.THIRDERR


class IoError(APIHTTPException):  # 文件读写错误
    code = 200
    status_code = RET.IOERR


class ServerError(APIHTTPException):  # 服务器内部错误
    code = 200
    status_code = RET.SERVERERR


class UnknownError(APIHTTPException):  # 未知错误
    code = 200
    status_code = RET.UNKOWNERR
