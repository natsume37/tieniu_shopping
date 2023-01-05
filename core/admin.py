"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : admin.py
@Author : 夏目&青一
@Time : 2023/1/4 20:40

"""
"""
管理员试图
"""

from core import src
from interface import admin_interface

# 添加账户功能
def add_user():
    is_admin = input('是否添加为管理员(y / n)').strip().lower()
    if is_admin == 'y':
        src.register(True)
    else:
        src.register()


# 冻结账号功能
def lock_user():
    while True:
        # 1、接受管理员输入的密码
        lock_username = input('请输入需要冻结的用户名：').strip()
        # 1.2、判断是否为管理员

        is_lock = input('按任意键确认/n退出：').strip().lower()

        # 2、判断是否需要退出
        if is_lock == 'n':
            break

        # 调用冻结接口、冻结账号
        flag, msg = admin_interface.lock_user_interface(lock_username)
        print(msg)
        if flag:
            break


# 给用户充值
def recharge_to_user():
    username = input('请输入需要充值的用户名：').strip()
    src.recharge(username)


func_dic = {
    '0': ('返回首页',),
    '1': ('添加账户', add_user),
    '2': ('冻结账户', lock_user),
    '3': ('用户充值', recharge_to_user),
}


def main():
    while True:
        print('管理员功能'.center(20, '='))
        for num in func_dic:
            print(f'{num}  {func_dic.get(num)[0].center(20, " ")}')
        print('我是有底线的'.center(20, '='))
        opt = input('请输入功能编号--> ').strip()
        if opt not in func_dic:
            print('\033[33m此功能不存在\033[0m')
            continue
        if opt == '0':
            break
        func_dic.get(opt)[1]()
