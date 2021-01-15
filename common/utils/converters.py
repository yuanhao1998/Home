# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:34
# @Author   : yuan hao

"""
在此编写所有自定义路由转换器
用于获取路径参数
eg: /app/user/<mobile>
"""

import inspect
import sys

import re
from werkzeug.routing import BaseConverter


class MobileConverter(BaseConverter):  # 手机号验证
    regex = r'1[3-9]\d{9}$'

    def to_url(self, value):
        return value

    def to_python(self, value):
        return value


def register_converters(app):
    """
    此方法用于动态注册路由转换器，使用者只需写好路由转换器类即可。
    默认注册路由名为小写的类名截取，例：MobileConverter 会自动注册为 mobile
    :param app: flask对象
    :return:
    """
    cls_list = inspect.getmembers(sys.modules[__name__], inspect.isclass)  # 获取当前文件所有类名
    for cls_name, cls in cls_list:
        if cls_name != 'BaseConverter':  # base路由不注册
            re_name = re.match('.*(?=Converter)', cls_name)  # 从类名中截取需要的部分
            url_name = str.lower(re_name.group())
            app.url_map.converters[url_name] = cls_name  # 注册到app中
