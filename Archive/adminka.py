#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql.cursors

def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def add_admin(**param): # Add a new Vodomat
    connection = connect()
    cursor = connection.cursor()
    first = "INSERT INTO admin (idv, idT, rules) values (%s,%s,%s)"
    second = (param.get('idv'), param.get('idT'), param.get('rules'))
    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()
    return True

def update_admin(**kwargs):
    connection = connect()
    cursor = connection.cursor()
    first = "UPDATE admin SET idT = %s, rules = %s WHERE idv = %s"
    print('HIIIIIII')
    second = (kwargs.get('idT'), kwargs.get('rules'), kwargs.get('idv'))
    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()

def get_admin(idv): # Get a Vodomat with its idv
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admin WHERE idv = %i" % (idv))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results
