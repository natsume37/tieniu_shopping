"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : src.py.py
@Author : 夏目&青一
@Time : 2023/1/4 1:35

"""
"""
用户视图层代码
"""

from interface import user_interface, bank_interface, shop_interface
from lib import common

# 定义登录状态
logged_user = None
# 定义管理员状态
logged_admin = False


# 0、退出
def sign_out():
    print('感谢使用，欢迎下次光临')
    exit()


# 1、注册功能
def register(is_admin=False):
    while True:
        print('\n注册')
        # 1.输入用户名和密码
        username = input('请输入用户名：').strip()

        # 2.3、校验用户名是否合法
        import re
        # if re.findall('^[a-zA-Z]\w{2,9}$', username):
        #     print('\n用户名长度必须为3-10个字符！\n只能由字母、数字、下划线组成')
        #     continue

        password = input('请输入密码：').strip()

        # 2.4、校验密码强度

        if not re.findall('^(?=.*[A-Z])(?=.*[a-z])(?=.*[\d]).{8,16}$', password):
            print('密码太弱,必须包含大写字母小写字母以及数字，并且长度在8-16位')
            continue

        re_password = input('请重新输入密码：').strip()
        is_register = input("按任意键确认/n退出：").strip().lower()

        # 2、进行简单的逻辑判断
        # 2.1、判断用户是否退出
        if is_register == 'n':
            break

        # 2.2、判断两次输入的密码是否一致
        if password != re_password:
            print('\n两次输入密码不一致！')
            continue

        # 3、密码加密
        password = common.pwd_to_sha256(password)

        # 调用注册接口进行注册
        flag, msg = user_interface.register_interface(username, password, is_admin)
        print(msg)
        if flag:
            break


# 2、登录功能
def login():
    while True:
        print('\n登录')
        # 1、让用户输入用户名和密码
        username = input('请输入用户名-->').strip()
        password = input('请输入密码-->').strip()
        is_login = input('按任意键确认/n键退出-->').strip().lower()

        # 2、判断用户是否退出
        if is_login == 'n':
            break

        # 3、密码加密
        password = common.pwd_to_sha256(password)

        # 4、调用接口层、把数据传给登录接口、让接口层调用数据层校验用户是否已存在
        flag, msg, is_admin = user_interface.login_interface(username, password)
        print(msg)
        if flag:
            global logged_user, logged_admin
            logged_user = username
            logged_admin = is_admin
            break


# 3、充值功能
@common.login_auth
def recharge(username=False):
    while True:
        print('\n充值')
        # 1、接受用户输入的充值金额
        amount = input('请输入充值金额：').strip()
        is_recharge = input('按任意键确认/n退出：').strip()
        # 2、判断是否退出
        if is_recharge == 'n':
            break

        # 3、判断用户输入的是否为数字
        if not amount.isdigit():
            print('\n请输入正确的金额')
            continue

        # 4、把amount转成int类型
        amount = int(amount)

        # 5、判断用户输入是否为0
        if amount == 0:
            print('充值金额应大于0！！')
            continue

        # 6、调用充值接口进行充值
        if not username:
            username = logged_user
        flag, msg = bank_interface.recharge_interface(username, amount)
        print(msg)
        if flag:
            break


# 4、转账功能
@common.login_auth
def transfer():
    while True:
        print('\n转账')
        # 1、接受用户输入的用户名和转账记录
        to_username = input('请输入转账目标的用户名：').strip()
        amount = input('请输入转账金额：').strip()
        is_transfer = input('按任意键确认/n退出：').strip().lower()

        # 2、判断是否退出
        if is_transfer == 'n':
            break

        # 3、判断用户输入的是否为数字
        if not amount.isdigit():
            print('\n请输入正确的金额')
            continue

        # 4、把amount转成int类型
        amount = int(amount)

        # 5、判断用户输入是否为0
        if amount < 0:
            print('\n转账的金额不能为0！！')
            continue

        # 6、判断用户是否在给自己转账
        if logged_user == to_username:
            print('\n不能给自己转账')
            continue

        # 7、调用转账接口
        flag, msg = bank_interface.transfer_interface(
            logged_user,
            to_username,
            amount
        )
        print(msg)
        if flag:
            break


# 5、提现功能
@common.login_auth
def withdraw():
    print('\n提现')
    while True:
        # 1、接受用户输入的提现金额
        amount = input('请输入提现金额：').strip()
        is_withdraw = input('按任意键确认/n退出：').strip().lower()
        # 2、判断是否退出
        if is_withdraw == 'n':
            break

        # 3、判断用户输入的是否为数字
        if not amount.isdigit():
            print('\n请输入正确的金额')
            continue

        # 4、把amount转成int类型
        amount = int(amount)

        # 5、判断用户输入是否为0
        if amount < 100:
            print('提现金额应大于100！！')
            continue

        # 6、调用提现接口进行充值
        flag, msg = bank_interface.withdraw_interface(logged_user, amount)
        print(msg)
        if flag:
            break


# 6、查看余额
@common.login_auth
def check_balance():
    print('\n查看余额')
    flag, msg = bank_interface.check_balance_interface(logged_user)
    print(msg)


# 7、查看流水功能
@common.login_auth
def check_flow():
    print('查看流水')
    flag, flow_list = bank_interface.check_flow_interface(logged_user)
    if not flow_list:
        print('\n当前用户没有流水')
    for flow in flow_list:
        print(flow, end='')
        print()


# 8、购物功能
@common.login_auth
def shopping():
    # 初始化购物车
    shopping_cart = {}

    # 1、调用接口层，获取商品数据
    goods = shop_interface.check_goods_interface('goods')

    if not goods:
        print('\n没有商品数据')
        return

    while True:
        print('欢迎来到铁牛商场'.center(50, '='))
        print(f'{"商品编号":<10}{"商品名称":<10}{"商品价格":<10}')
        # 枚举
        for indx, good in enumerate(goods):
            print(f'{indx+1:<10}{good.get("name"):<10}{good.get("price"):<10}')
        print('24小时为你服务'.center(50, '='))

        opt = input('请选择商品编号(y结算/n退出)：').strip()

        # 如果opt等于n，调用添加到购物车接口，把购物车数据写入文件
        if opt == 'n':
            if not shopping_cart:
                break
            flag, msg = shop_interface.add_shop_cart_interface(logged_user, shopping_cart)
            print(msg)
            if flag:
                break
        # 如果用户输入y，调用结算接口
        if opt == 'y':
            if not shopping_cart:
                print('\n没有选择任何商品，无法结算！')
                continue

            flag, msg, total = shop_interface.close_account_interface(logged_user, shopping_cart)
            print(msg)
            if flag:
                print('欢迎光临铁牛'.center(65, ' '))
                print('='*65)
                print(f'{"商品编号":<10}{"商品名称":<10}{"商品价格":<10}{"商品数量":<10}{"商品数量":<10}')
                for indx, good in enumerate(shopping_cart.values()):
                    print(f'{indx + 1:<10}{good.get("name"):<10}{good.get("price"):<10}{good.get("数量"):<10}')
                print(f'总消费金额：{total}')
                print('='*65)
                print('谢谢惠顾，欢迎下次光临'.center(65, ' '))
                print('请保管好您的小票'.center(65, ' '))
                break
            break

        # 3、判断用户输入的编号是否存在/用户输入的是否为数字
        if not opt.isdigit():
            print('\n请输入正确的商品编号')
            continue
        # 4、判断用户输入的序号是否存在
        opt = int(opt) - 1
        if opt not in list(range(len(goods))):
            print('\n该商品不存在！')
            continue

        # 5获取用户的商品信息
        good_info = goods[opt]
        name = good_info.get('name')

        # 6、把商品信息添加到购物车
        # 6.1、判断购物车是否有相同的商品
        if name not in shopping_cart:
            good_info['数量'] = 1
            shopping_cart[name] = good_info
        else:
            shopping_cart[name]['数量'] +=1

        print('\n当前购物车数据：')
        print(f'{"商品编号":<10}{"商品名称":<10}{"商品价格":<10}{"商品数量":<10}{"商品数量":<10}')
        # 枚举
        for indx, good in enumerate(shopping_cart.values()):
            print(f'{indx + 1:<10}{good.get("name"):<10}{good.get("price"):<10}{good.get("数量"):<10}')



        # 1）让用户继续选择商品
        # 2）让用户结算
        # 3）用户不想结算，想退出购物功能，把用户的购物车数据写入到用户数据






# 9、查看购物车
@common.login_auth
def check_shopping_cart():
    # 1、调用查看购物车接口
    shop_cart_file = shop_interface.check_shop_chart_interface(logged_user)
    if not shop_cart_file:
        print('\n你的购物车还没有东西！！')
        return

    print('\n当前购物车数据：')
    print(f'{"商品编号":<10}{"商品名称":<10}{"商品价格":<10}{"商品数量":<10}{"商品价格":<10}')
    for indx, good in enumerate(shop_cart_file.values()):
        print(f'{indx + 1:<10}{good.get("name"):<10}{good.get("price"):<10}{good.get("数量"):<10}{good.get("price")* good.get("数量"):<10}')

    opt = input('\ny购买/n退出/d删除商品').strip().lower()

    if opt == 'y':
        flag, msg, total = shop_interface.close_account_interface(logged_user, shop_cart_file)
        print(msg)
        if flag:
            # 调用更新购物车功能
            shop_interface.clear_shop_cart_interface(logged_user)

    # 结算失败则退出
    if opt == 'd':
        while True:
            opt1 = input('请输入你要删除的商品名/按非数字键退出').strip().lower()
            # 如果是数字则调用删除接口
            if opt1.isdigit():
                msg = shop_interface.delete_shopping_cart(logged_user, opt1)
                print(f'\n{msg} 已从购物车删除' \
                      f'当前购物车为')
            else:
                print('\n已退出购物车界面！')
                break

# 10、退出账号
@common.login_auth
def login_out():
    global logged_user, logged_admin
    print(f'\n用户{logged_user}  已退出！')
    logged_user = None
    logged_admin = False


# 11、管理员功能
@common.login_auth
def admin():
    from core import admin
    admin.main()


# 函数字典
func_dic = {
    '0': ('退出', sign_out),
    '1': ('注册功能', register),
    '2': ('登录功能', login),
    '3': ('充值功能', recharge),
    '4': ('转账功能', transfer),
    '5': ('提现余额', withdraw),
    '6': ('查看余额功能', check_balance),
    '7': ('查看流水', check_flow),
    '8': ('购物功能', shopping),
    '9': ('查看购物车', check_shopping_cart),
    '10': ('退出账号', login_out),
    '11': ('管理员功能', admin),
}


# 主程序
def main():
    while True:
        print('购物管理系统'.center(20, '='))
        for num in func_dic:
            if logged_admin:
                print(f'{num}  {func_dic.get(num)[0].center(20, " ")}')
            else:
                if num != '11':
                    print(f'{num}  {func_dic.get(num)[0].center(20, " ")}')
        print('我是有底线的'.center(20, '='))
        opt = input('请输入功能编号--> ').strip()
        if opt not in func_dic or (not logged_admin and opt == '11'):
            print('\033[33m此功能不存在\033[0m')
            continue
        func_dic.get(opt)[1]()
