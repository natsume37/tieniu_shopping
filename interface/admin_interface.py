"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : admin_interface.py
@Author : 夏目&青一
@Time : 2023/1/4 1:43

"""

"""
管理相关的接口
"""
from db import db_handler
from lib import common

logged = common.get_logger('admin')


# 冻结接口

def lock_user_interface(username):
    user_data = db_handler.select_data(username)

    # 2、判断用户是否存在
    if not user_data:
        return False, f'\n用户：{username} 不存在'

    if not user_data['is_admin']:
        if user_data.get('locked'):
            user_data['locked'] = False
            db_handler.save(user_data)

            msg = f'用户：{username} 已解冻！'
            logged.info(msg)

            return True, msg
        else:
            user_data['locked'] = True
            db_handler.save(user_data)

            msg = f'用户：{username} 已冻结！'
            logged.warning(msg)

            return True, msg

    msg1 = f'{username}为管理员账号，不能冻结!!'
    logged.warning(msg1)

    return True,