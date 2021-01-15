# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:13
# @Author   : yuan hao

from flask import Blueprint, current_app

common_bp = Blueprint('common', __name__)  # 公共蓝图，用于定义全局处理，例如：全局异常捕获等


@common_bp.route('/favicon.ico')  # 请求图标
def favicon():
    return current_app.send_static_file('favicon.ico')

