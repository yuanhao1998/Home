# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:33
# @Author   : yuan hao

"""
在此编写所有封装的公共方法
"""


def import_class(package):
    """
    此方法用于动态导入指定包名下所有类
    包需要放在common目录下
    :param package: 包名
    """
    import importlib
    import os

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + package
    files = os.listdir(path)
    for file in files:
        if not file.startswith("__"):
            module_name = ("." + os.path.splitext(file)[0])
            importlib.import_module(module_name, package=package)


def queryset_to_dict(queryset) -> dict:
    """
    此方法用于将模型类转换为字典
    支持的类型：模型类、模型类列表（包括paginate分页结果），原生sql查询得到的元组、元组列表
    :param queryset: 要转换的模型类
    :return: 对应的字典
    """

    from flask_sqlalchemy import Model, Pagination

    try:
        if isinstance(queryset, Pagination):  # 如果是分页结果集，获取items列表
            queryset = queryset.items

        if isinstance(queryset, list):
            if isinstance(queryset[0], Model):
                tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in queryset]
                for t in tmp:
                    t.pop('_sa_instance_state')
            else:
                tmp = [dict(zip(res._keymap.keys(), res._row)) for res in queryset]
        else:
            if isinstance(queryset, Model):
                tmp = dict(zip(list(queryset.__dict__.keys()), list(queryset.__dict__.values())))
                tmp.pop('_sa_instance_state')
            else:
                tmp = dict(zip(queryset._keymap.keys(), queryset._row))

        return tmp
    except Exception:
        raise TypeError('Unknown queryset type')


def check_params(args, params_list):
    """
    此方法用于校验参数是否完整
    :param args: 要校验的参数字典，eg：args = request.json
    :param params_list: 要校验的参数名称，eg：params_list = ['mobile', 'code_id']
    """
    from utils.exception import MissParamsError

    if not args:
        raise MissParamsError('没有获取到任何参数！')
    left = list(args.keys())
    left.sort()
    params_list.sort()

    if None in args.values() or left != params_list:
        raise MissParamsError('参数缺失！')


def send_sms(sms_code, mobile):
    """
    此方法用于发送短信验证码，使用腾讯云短信接口
    :param sms_code: 要发送的验证码
    :param mobile: 要发给哪些手机号，多个手机号使用列表
    :return: 发生状态
    """
    from tencentcloud.common import credential
    from tencentcloud.sms.v20190711 import sms_client, models

    from utils.constants import TENCENT_SECRET_ID, TENCENT_SECRET_KEY, SMS_SDK_APPId, SMS_SIGN, SMS_TEMPLATE_ID, \
        SMS_CODE_EXPIRED_TIME_MINUTE

    cred = credential.Credential(TENCENT_SECRET_ID, TENCENT_SECRET_KEY)
    client = sms_client.SmsClient(cred, "ap-guangzhou")
    req = models.SendSmsRequest()
    req.SmsSdkAppid = SMS_SDK_APPId
    req.Sign = SMS_SIGN
    req.PhoneNumberSet = mobile if isinstance(mobile, list) else [mobile]
    req.TemplateID = SMS_TEMPLATE_ID
    req.TemplateParamSet = [sms_code, SMS_CODE_EXPIRED_TIME_MINUTE]
    result = client.SendSms(req)
    return result
