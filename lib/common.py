"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : common.py
@Author : 夏目&青一
@Time : 2023/1/4 1:45

"""

"""
公共方法
"""
import logging.config
from conf import settings


# 密码加密
def pwd_to_sha256(password):
    import hashlib
    sha = hashlib.sha256()
    sha.update(password.encode('utf-8'))
    # 密码加盐
    sha.update('natsume'.encode('utf-8'))
    return sha.hexdigest()


# 登录认证装饰器
def login_auth(func):
    def wrapper(*args, **kwargs):
        from core import src
        # 登录状态为Ture时
        if src.logged_user:
            res = func(*args, **kwargs)
            return res
        else:
            print('\n你个憨憨，要先登录！！！')
            src.login()

    return wrapper


# 日志记录功能

def get_logger(logger_name):
    # 1、加载日志配置字典
    logging.config.dictConfig(settings.LOGGING_DIC)

    # 2、获取logger
    logger = logging.getLogger(logger_name)
    return logger