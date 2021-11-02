#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
mail.py: email server utils
'''

import sys
import argparse
import getpass
from os import getenv

try:
    import mysql.connector as mariadb
except ImportError:
    print('找不到 mysql 客户端，请安装: pip install mysql-connector-python')
    sys.exit(2)


_version = '2.1'

parser = argparse.ArgumentParser(description='作用: 插入邮件、删除邮件、查看邮箱、修改密码')
parser.add_argument(
    '-v',
    '--version',
    action='version',
    version=f"%(prog)s version: {_version}",
    help='显示版本并退出'
)
args = parser.parse_args()

username = getenv('DB_USERNAME')
password = getenv('DB_PASSWORD')
dbname = getenv('DB_DATABASE')
dbhost = getenv('DB_HOST')

try:
    conn = mariadb.connect(
        host=dbhost,
        user=username,
        passwd=password,
        database=dbname,
        use_pure=True
)
except mariadb.Error as err:
    print("Error: {}".format(err))
    sys.exit(0)

all_mails = []
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
myresult = cursor.fetchall()

for x in myresult:
    all_mails.append(x[0])

prompt_text = """\
    0.退出
    1.新建邮箱
    2.删除邮箱
    3.显示所有邮箱
    4.修改密码
    5.显示可用邮箱域名
    输入数字:
"""

var1 = input(prompt_text)
while var1 != "0":
    # 插入邮箱
    if var1 == "1":
        str0 = input("输入新邮箱: ")
        print("输入的内容是: ", str0)

        print("输入密码: ")
        str1 = getpass.getpass()
        print(("再次输入密码: "))
        str_1 = getpass.getpass()
        if str1 != str_1:
            print("再次密码不一样")
            continue
        try:
            cursor = conn.cursor(prepared=True)
            val = (str0, str1)
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ENCRYPT(?))", val)
            conn.commit()
            print (cursor.rowcount, "个邮箱已插入")

        except mariadb.Error as error:

            print("Error: {}".format(error))
            input("Press Enter to continue...")

    # 删除邮箱
    elif var1 == "2":

        str2 = input("输入删除的邮箱: ")
        if str2 not in all_mails:
            print(str2, "不存在")
            input("Press Enter to continue...")
        else:

            try:
                cursor = conn.cursor(prepared=True)
                sql1 = "DELETE FROM users WHERE email = %s"
                val1 = (str2)
                cursor.execute(sql1, (val1,))
                conn.commit()
                print (str2, "已删除")
            except mariadb.Error as error:
                print("Error: {}".format(error))
                input("Press Enter to continue...")

    # 显示所有邮箱
    elif var1 == "3":
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users")
        myresult = cursor.fetchall()
        for x in myresult:
            print(x[0])

    # 修改密码
    elif var1 == "4":
        str3 = input("输入邮箱: ")
        print("输入的内容是: ", str3)
        str4 = getpass.getpass("输入新密码: ")
        str_4 = getpass.getpass("再次输入密码: ")
        if str4 != str_4:
            print("两次密码不一样")
            continue

        try:
            cursor = conn.cursor(prepared=True)
            val2 = (str4, str3)
            cursor.execute("UPDATE users SET password = ENCRYPT(?) WHERE email = ?", val2)
            conn.commit()
            print(str3, "密码已修改")
        except mariadb.Error as error:
            print("Errot: {}".format(error))
            input("Press Enter to continue...")

    # 显示可用域名
    elif var1 == "5":
        cursor = conn.cursor()
        cursor.execute("SELECT domain FROM domains")
        myresult = cursor.fetchall()
        for x in myresult:
            print(x[0])
    else:
        print("请输入有效数字")
        input("Press Enter to continue...")
    input("Press Enter to continue...")
    var1 = input(prompt_text)
