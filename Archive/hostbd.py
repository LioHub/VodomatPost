#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql.cursors
import time

def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection




def add_host(idv): # Add a new Vodomat
  result=get_vodomat(idv)

  if result is None or int(result['idv']) != int(idv):
    param = {"idv": 0, "State": "", "input10Counter": 0, "out10Counter": 0,"milLitlose": 0,
                 "milLitWentOut": 0, "milLitContIn": 0, "waterPrice": 0, "contVolume": 0, "totalPaid": 0, "sessionPaid": 0,
                 "leftFromPaid": 0, "container": "", "currentContainerVolume": "",
                 "consumerPump": 0, "mainPump": 0, "magistralPressure": 0, "mainValve": 0,
                 "filterValve": 0, "washFilValve": 0, "tumperMoney": 0, "tumperDoor": 0,
                 "serviceButton": 0, "freeButton": 0, "Voltage": 0, 'cashing': 0, 'credit': 0, 'sale': 0}
    param["idv"]=idv
    connection = connect()
    cursor = connection.cursor()
    first = "INSERT INTO vs (idv, State, input10Counter, out10Counter, milLitlose, milLitWentOut, milLitContIn, waterPrice, contVolume, totalPaid, sessionPaid, leftFromPaid, container, currentContainerVolume, consumerPump, mainPump, magistralPressure, mainValve, filterValve, washFilValve, tumperMoney, tumperDoor, serviceButton, freeButton, Voltage, cashing, credit, sale, containerMinVolume, billAccept, maxContainerVolume, stateGraph, containerGraph) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    second = (param.get('idv'), param.get('State'), param.get('input10Counter'), param.get('out10Counter'), param.get('milLitlose'), param.get('milLitWentOut'), param.get('milLitContIn'), param.get('waterPrice'), param.get('contVolume'), param.get('totalPaid'), param.get('sessionPaid'), param.get('leftFromPaid'), param.get('container'), param.get('currentContainerVolume'), param.get('consumerPump'), param.get('mainPump'), param.get('magistralPressure'), param.get('mainValve'), param.get('filterValve'), param.get('washFilValve'), param.get('tumperMoney'), param.get('tumperDoor'), param.get('serviceButton'), param.get('freeButton'), param.get('Voltage'),
              param.get('cashing'), param.get('credit'), param.get('sale'),
              param.get('containerMinVolume'), param.get('billAccept'), param.get('maxContainerVolume'), param.get('stateGraph'), param.get('containerGraph'))
    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  return False

def add_hostVVS(**param): # Add a new Vodomat
  # result=get_vodomatVVS(param['idv'])
  # print('dfd')
  # if result is None or int(result['idv']) != int(param['idv']):
    connection = connect()
    cursor = connection.cursor()
    print('intoif')
    first = "INSERT INTO vss (idv, totalPaid, sessionPaid, leftFromPaid, cashing, credit, sale) values (%s,%s,%s,%s,%s,%s,%s)"
    print('after_exe')
    second = (param.get('idv'), param.get('totalPaid'), param.get('sessionPaid'), param.get('leftFromPaid'), param.get('cashing'), param.get('credit'), param.get('sale'))
    print('after_exe')
    cursor.execute(first, second)
    print('after_exe')
    connection.commit()
    cursor.close()
    connection.close()
    print('after_commit')
    return True
  # return False




# #Get DATABASE
def get_vodomat(idv): # Get a Vodomat with its idv
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vs WHERE idv = %i" % (idv))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

# #Get DATABASE
def get_vodomat2(idv): # Get a Vodomat with its idv
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT mainValve, magistralPressure, idv, serviceButton, milLitWentOut, Voltage, input10Counter, leftFromPaid,  currentContainerVolume, containerMinVolume, freeButton, sessionPaid, tumperDoor, tumperMoney, filterValve, washFilValve, billAccept, milLitlose, waterPrice, mainPump, maxContainerVolume, contVolume, container, out10Counter, stateGraph, containerGraph, milLitContIn, consumerPump, State, totalPaid FROM vs WHERE idv = %i" % (idv))

    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

# #Get DATABASE
def get_vodomatVVS(idv): # Get a Vodomat with its idv
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vss WHERE idv = %i" % (idv))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results




#waterPrice
def add_waterPrice(message, idv):
    connect = connection.connect()
    cursor = connect.cursor()
    cursor.execute("UPDATE vs SET waterPrice = %i  WHERE idv = %i" % (int(message.text), int(idv)))
    connect.commit()
    cursor.close()
    connect.close()

#UPDATE DATABASE
def update_vodomat(**param):
    connection = connect()
    cursor = connection.cursor()
    print('3')
    lastsave = time.time()
    first = "UPDATE vs SET State = %s, input10Counter = %s, out10Counter = %s, milLitlose = %s, milLitWentOut = %s, milLitContIn = %s, waterPrice = %s, contVolume = %s, totalPaid = %s, sessionPaid = %s, leftFromPaid = %s, container = %s, currentContainerVolume = %s, consumerPump = %s, mainPump = %s, magistralPressure = %s, mainValve = %s, filterValve = %s, washFilValve = %s, tumperMoney = %s, tumperDoor = %s, serviceButton = %s, freeButton = %s, Voltage = %s, billAccept = %s, containerGraph = %s, containerMinVolume = %s, stateGraph = %s, maxContainerVolume = %s, lastsave = %s WHERE idv = %s "
    second = (param.get('State'), param.get('input10Counter'),param.get('out10Counter'),param.get('milLitlose'),param.get('milLitWentOut'),param.get('milLitContIn'),param.get('waterPrice'),param.get('contVolume'),param.get('totalPaid'),param.get('sessionPaid'),param.get('leftFromPaid'),param.get('container'),param.get('currentContainerVolume'),param.get('consumerPump'),param.get('mainPump'),param.get('magistralPressure'),param.get('mainValve'),param.get('filterValve'),param.get('washFilValve'),param.get('tumperMoney'),param.get('tumperDoor'),param.get('serviceButton'),param.get('freeButton'),param.get('Voltage'), param.get('billAccept'), param.get('containerGraph'), param.get('containerMinVolume'), param.get('stateGraph'), param.get('maxContainerVolume'), lastsave, param['idv'])
    try:
        cursor.execute(first, second)
    except:
        cursor.close()
        connection.close()
        raise Exception
    else:
        print('4')
        connection.commit()
        cursor.close()
        connection.close()
        print('5')
        return True

#UPDATE LastSave
def update_vodomatTime(idv):
        connection = connect()
        cursor = connection.cursor()
        print('3')
        lastsave = time.time()
        first = "UPDATE vs SET lastsave = %s WHERE idv = %s "
        second = (lastsave, idv)
        try:
            cursor.execute(first, second)
        except:
            cursor.close()
            connection.close()
            raise Exception
        else:
            connection.commit()
            cursor.close()
            connection.close()
            return True

# UPDATE reserve
def update_vodomatReserve(Reserve, idv):
        connection = connect()
        cursor = connection.cursor()
        print('3')
        first = "UPDATE vs SET Reserve = %s WHERE idv = %s "
        second = (Reserve, idv)
        try:
            cursor.execute(first, second)
        except:
            cursor.close()
            connection.close()
            raise Exception
        else:
            print('4')
            connection.commit()
            cursor.close()
            connection.close()
            print('5')
            return True

#UPDATE DATABASE
def update_vodomatVVS(**param):
    connection = connect()
    cursor = connection.cursor()
    print("sdfsdfssfsdfsdf")
    first = "UPDATE vss SET totalPaid = %s, sessionPaid = %s, leftFromPaid = %s, sale = %s, cashing = %s, credit = %s WHERE idv = %s "
    second = (param.get('totalPaid'), param.get('sessionPaid'),param.get('leftFromPaid'), param.get('sale'), param.get('cashing'), param.get('credit'), param['idv'])
    try:
        cursor.execute(first, second)
    except Exception as e:
        print("Exception update -> %s, sql -> first %s, second -> %s" % (e, first, second))
    print("dsafsad")
    connection.commit()
    cursor.close()
    connection.close()
    print("sdsdsd")
    return True

def update_vodomatScore(idv, score): # Get a Vodomat with its idv
    connection = connect()
    cursor = connection.cursor()
    print("into hostbd where been upvodscore:")
    print("idv:")
    print(idv)
    print("score:")
    print(score)
    first = "UPDATE vs SET cashing = %s, credit = %s, sale = %s WHERE idv = %s"
    second = (score.get('cashing'), score.get('credit'), score.get('sale'), idv)
    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()

def update_vodomatActivate(idv, Activate): # Get a Vodomat with its idv
    connection = connect()
    cursor = connection.cursor()
    print("into hostbd where been upvodscore:")
    print("idv:")
    print(idv)
    print("Activate:")
    print(Activate)
    first = "UPDATE vs SET action = %s WHERE idv = %s"
    second = (Activate, idv)
    cursor.execute(first, second)
    connection.commit()
    cursor.close()
    connection.close()




# DELETE VODOMAT
def delete_vodomat(idv):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE from vs where idv = %i" % (idv))
    connection.commit()
    cursor.close()
    connection.close()
    return True

# DELETE VODOMAT
def delete_vodomatVVS(idv):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE from vss where idv = %i" % (idv))
    connection.commit()
    cursor.close()
    connection.close()
    return True