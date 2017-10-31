#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import random
# import sqlite3
# conn = sqlite3.connect('Vodm.db')
# c = conn.cursor()

def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# Функция для добавления пользователя
def add_user(uid, uname):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT idT FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    print('result:')
    print(results)

    if results is None or str(results['idT']) != str(uid):
        List = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(List)
        a = ''
        i = 0
        while List is not None:
            try:
                a = a + str(List[i])
                i = i + 1
            except Exception as e:
                print(a)
                break
        cursor.execute("INSERT INTO users (idT, name, score, promocode) values ( %i, '%s', %i, %s)" % (uid, uname, 0, str(a)))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    cursor.close()
    connection.close()
    return False

# Функция для обновления счета
def update_user(**kwargs):
    connection = connect()
    cursor = connection.cursor()

    first = "UPDATE users SET score = %s, idv = %s WHERE idT = %s"
    second = (kwargs.get('score'), kwargs.get('idv'), kwargs.get('idT'))

    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()

def update_useridv(**param):
    connection = connect()
    cursor = connection.cursor()

    first = "UPDATE users SET idv = %s WHERE idT = %s"
    second = (param.get('idv'), param.get('idT'))

    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()

# Функция для обновления монеты
def update_userAfterGotMoney(**kwargs):
    connection = connect()
    cursor = connection.cursor()

    first = "UPDATE users SET cashing = %s, credit = %s, sale = %s WHERE idT = %s"
    second = (kwargs.get('cashing'), kwargs.get('credit'), kwargs.get('sale'), kwargs.get('idT'))

    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()

# Функция для ввода промока кода
def insert(idT, promo):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT idT FROM users WHERE promocode = %s" % (str(promo)))
    results = cursor.fetchone()
    print('result:')
    print(results)

    print('idT:')
    print(idT)

    print('promo:')
    print(promo)

    promoOW = get_user(idT)
    print("promoOW")
    print(promoOW)
    try:
        if int(results['idT']) == int(idT) or promoOW['inviter'] !='':
            print('no2323232 False')
            cursor.close()
            connection.close()
            return False
    except:
        pass



    if results is not None:
    # connection = connect()
    # cursor = connection.cursor()
        first = "UPDATE users SET inviter = %s WHERE idT = %s"
        # second = (kwargs.get('score'), kwargs.get('idT'))
        print('HIIIIIII')
        second = (str(promo), idT)
        cursor.execute(first, second)
        connection.commit()
        cursor.close()
        connection.close()
        print('ok True')
        return True

    cursor.close()
    connection.close()
    print('no False')
    return False

# Get a User with its idT
def get_user(idT):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE idT = %i" % (idT))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

# Get a User with its idT
def get_userV(idv):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE idv = %i" % (idv))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results