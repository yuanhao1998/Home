# -*- coding: utf_8 -*-
# @Time     : 2020/11/23 9:16
# @Author   : yuan hao

from app import create_app

app = create_app('dev')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
