"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : settings.py.py
@Author : 夏目&青一
@Time : 2023/1/4 1:47

"""

"""
配置信息
"""

# 获取项目根目录
import os
import configparser
from lib import common

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

# 获取日志存放路径
LOG_DIR = os.path.join(
    BASE_DIR, 'log'
)

# 日志配置字典
LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # 日志格式
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s [%(name)s] %(levelname)s  %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'test': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'filters': {},
    # 日志处理器
    'handlers': {
        'console_debug_handler': {
            'level': 'DEBUG',  # 日志处理的级别限制
            'class': 'logging.StreamHandler',  # 输出到终端
            'formatter': 'simple'  # 日志格式
        },
        'file_user_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': os.path.join(LOG_DIR, 'user.log'),
            'maxBytes': 1024 * 1024 * 10,  # 日志大小 10M
            'backupCount': 10,  # 日志文件保存数量限制
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'file_bank_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': os.path.join(LOG_DIR, 'bank.log'),
            'maxBytes': 1024 * 1024 * 10,  # 日志大小 10M
            'backupCount': 10,  # 日志文件保存数量限制
            'encoding': 'utf-8',
            'formatter': 'standard',
        },

    },
    # 日志记录器
    'loggers': {
        '': {  # 导入时logging.getLogger时使用的app_name
            'handlers': ['file_user_handler'],  # 日志分配到哪个handlers中
            'level': 'INFO',  # 日志记录的级别限制
            'propagate': False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
        },
        'bank_logger': {
            'handlers': ['file_bank_handler'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

CONFIG_PATH = os.path.join(
    BASE_DIR, 'settings.cfg'
)

logger = common.get_logger('严重错误')
if not os.path.exists(CONFIG_PATH):
    logger.critical('配置文件丢失！')
    exit()

# 获取USER_DATA路径
CONFIG_PATH = os.path.join(
    BASE_DIR, 'settings.cfg'
)

config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding='utf-8-sig')  # 带有签名的utf-8
USER_DATA_DIR = config.get('path', 'USER_DATA_DIR')

if not os.path.isdir(USER_DATA_DIR):
    # 拼接路径  (若路径不存在则使用默认路径)
    USER_DATA_DIR = os.path.join(
        BASE_DIR, 'db', 'user_data'
    )

# 获取goods_data路劲
GOODS_DATA_DIR = os.path.join(
    BASE_DIR, 'db', 'goods_data'
)

# 获取提现手续费
RATE = config.getfloat('bank', 'RATE')
