"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : bank_interface.py
@Author : 夏目&青一
@Time : 2023/1/4 1:41

"""

"""
银行相关的接口
"""
from datetime import datetime
from db import db_handler
from conf import settings
from lib import common

logger = common.get_logger('bank_logger')


# 充值接口
def recharge_interface(username, amount):
    # 1、获取用户数据
    user_data = db_handler.select_data(username)

    if not user_data:
        return True, f'\n用户{username} 不存在！'
    # 2、给user_data里面的balance加钱
    user_data['balance'] += amount

    # 3、记录流水
    msg = f'{datetime.now()}用户{username}充值 {amount} 成功！当前余额为：{user_data.get("balance")}'
    user_data['flow'].append(msg)

    # 4、调用用户处理层，保存修改后的数据
    db_handler.save(user_data)

    logger.info(msg)

    return True, msg


# 提现接口
def withdraw_interface(username, amount):
    # 1、获取用户数据
    user_data = db_handler.select_data(username)
    balance = user_data.get('balance')
    # 2、计算手续费，并判断余额是否充足
    service_fee = settings.RATE * amount
    if balance < (service_fee + amount):
        return False, f'你个穷鬼，提现失败'

    # 3、给user_data里面的balance扣钱
    user_data['balance'] -= (amount + service_fee)

    # 4、记录流水
    msg = f'\n{datetime.now()}-用户{username}提现了{amount}元' \
          f'手续费为{service_fee}元' \
          f'当前余额为：{user_data.get("balance")}元'

    if balance < amount:
        print('账户余额不足，请重新输入')

    # 4、调用用户处理层，保存修改后的数据
    db_handler.save(user_data)

    logger.info(msg)

    return True, msg


# 查看余额功能接口
def check_balance_interface(username):
    user_data = db_handler.select_data(username)
    balance = user_data.get('balance')
    return True, f'\n用户 {username}的余额为{balance}元'


# 转账接口
def transfer_interface(username, to_username, amount):
    # 1、获取两个用户的信息
    user_data = db_handler.select_data(username)
    to_user_data = db_handler.select_data(to_username)

    # 2、判断转账对象是否存在
    if not to_user_data:
        return False, f'\n目标用户：{to_user_data}  不存在'

    # 3、判断当前用户账户余额是否充足
    if user_data.get('balance') < amount:
        return False, '\n余额不足转账失败！',

    # 4、开始转账、给用户账户做加减
    user_data['balance'] -= amount
    to_user_data['balance'] += amount

    # 5、当前余额
    msg = f'\n{datetime.now()} 用户{username}给用户{to_username}转账成功!' \
          f'余额为{user_data["balance"]}元'
    user_data['flow'].append(msg)

    to_msg = f'\n{datetime.now()} 用户{to_username}收到用户{username}转账成功!' \
             f'余额为{to_user_data.get("balance")}元'
    to_user_data['flow'].append(to_msg)

    # 5、保存数据
    db_handler.save(user_data)
    db_handler.save(to_user_data)

    logger.info(msg)

    return True, msg


# 查看流水功能
def check_flow_interface(username):
    username_data = db_handler.select_data(username)
    flow_list = username_data.get('flow')
    return True, flow_list


# 支付接口
def pay_interface(username, total):
    user_data = db_handler.select_data(username)

    # 2、判断用户余额是否充足
    if user_data.get('balance') < total:
        msg = f'{username}余额不足,支付：{total} 元，失败！'
        logger.warning(msg)

        return False, msg

    # 3、支付
    user_data['balance'] -= total
    msg = f'\n{datetime.now()} 用户：{username} 消费：{total} 元，' \
          f'当前余额为：{user_data.get("balance")}'

    user_data['flow'].append(msg)

    # 5、保存用户数据
    db_handler.save(user_data)

    logger.info(msg)

    return True, msg
