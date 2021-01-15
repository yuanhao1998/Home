# -*- coding: utf_8 -*-
# @Time     : 2020/12/7 11:12
# @Author   : yuan hao
"""
在此编写所有参数校验方法
"""
import imghdr
import re

from utils.exception import ParamsTypeError


def check_email_type(email_str):
    """
    检验邮箱格式
    :param email_str: str 被检验字符串
    :return: email_str
    """
    if re.match(r'^([A-Za-z0-9_\-.\u4e00-\u9fa5])+@([A-Za-z0-9_\-.])+\.([A-Za-z]{2,8})$', email_str):
        return email_str
    else:
        raise ParamsTypeError('{} is not a valid email'.format(email_str))


def check_mobile_type(mobile_str):
    """
    检验手机号格式
    :param mobile_str: str 被检验字符串
    :return: mobile_str
    """
    if re.match(r'^((\+86)|(86))?[1][3-9][0-9]{9}$', mobile_str):
        return mobile_str
    else:
        raise ParamsTypeError('{} is not a valid mobile'.format(mobile_str))


def check_id_type(value):
    """检查是否为身份证号"""
    id_number_pattern = r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[' \
                        r'0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$) '
    if re.match(id_number_pattern, value):
        return value.upper()
    else:
        raise ParamsTypeError('Invalid id number.')


def check_image_type(value):
    """
    检验图片格式
    :param value: image 被检验图片
    :return: value
    """
    try:
        if imghdr.what(value):
            return value
        raise
    except Exception:
        raise ParamsTypeError('image type error')
