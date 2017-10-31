import threading
import socket
import json
import telebot
from telebot import types
import time
import billing

file = open("/opt/key.json")
# text = file.read()
# config = json.loads(text)
# token = config["token"]

token = json.loads(file.read())["token"]
bot = telebot.TeleBot(token)



from Archive import workbyfile
from Archive import hostbd
from Archive import userbd
from Archive import adminka

tableSock = {}

def cod(data):
    if type(data) == str:
        data = data.encode("utf-8")
    elif type(data) == dict:
        data = json.dumps(data).encode("utf-8")
    return data

def send(data, idv):
    data = cod(data)
    tableSock[int(idv)]["socket"].send(data)
    print("end send")

i=0
def connect(sock, addr):
    while True:
        data = json.loads(sock.recv(2048).decode("utf-8"))
        # data = data.decode("utf-8")

        if data is None:
            print("Disconnect. Not Data: ", addr)
            return False

        # data = json.loads(data)
        try:
            method = data.get("method")
            param = data.get("param")
            # print('method:')
            # print(method)
            # print('param:')
            # print(param)
            if method == "Start":
                print("Activate:")
                print(date)
                global i
                hostWI = hostbd.get_vodomat(int(param['idv']))
                print('hostWI:')
                print(hostWI)
                if hostWI['State'] == 'WAIT':
                    # LastTime =
                    if (hostWI['lasttime'] - 10) < time.time():
                        if hostWI['action'] == '0':
                            hostbd.update_vodomatReserve(hostWI['leftFromPaid'], hostWI['idv'])
                            print('Hi')
                            try:
                                print()
                                userbd.update_user(**param)
                                perTrue = "1"
                                idv = param['idv']
                                i = 0
                                hostbd.update_vodomatActivate(idv, perTrue)
                                send(date, idv)

                                Get_points = types.ReplyKeyboardMarkup()
                                Get_points.row("Остановить")

                                userbd.update_useridv(**param)

                                bot.send_message(param['idT'], "Вы успешно подключились к водомату", reply_markup = Get_points)
                                text_water = "Подключение прошло успешно\n\n1. Поднесите тару к водомату\n\n2. Нажмите кноку \"Старт\" на аппарате.\n\n Цена за 1 литр 4₽\n\nЧтобы пополнить баланс используйте купюроприемник и монетоприемник."
                                bot.send_message(param['idT'], text_water)
                                try:
                                    hostbd.add_hostVVS(**hostWI)
                                except:
                                    hostbd.update_vodomatVVS(**hostWI)
                            except Exception as e:
                                print("Exception %s" % e)
                                idv = param['idv']
                                perFalse = "0"
                                hostbd.update_vodomatActivate(idv, perFalse)

                                param['idv'] = 0
                                userbd.update_useridv(**param)

                                # Вывод кнопок
                                Get_points = types.ReplyKeyboardMarkup()
                                Get_points.row("Подключиться к водомату")
                                Get_points.row("Личный кабинет")

                                bot.send_message(param['idT'],
                                                 "Приносим вам свои извинения,"
                                                 "но водомат временно  не работает (;", reply_markup = Get_points)
                        else:
                            bot.send_message(param['idT'],
                                             "Пожалуйста, подождите, водомат пока занимет другой человек, ожидайте окончания сеанса его работы")
                    else:

                         bot.send_message(param['idT'],"Нет связи с водоматом")
                else:
                    bot.send_message(param['idT'],
                                     "Приносим вам свои извинения,"
                                     "но водомат временно  не работает (;")

            elif method == "Stop":
                print("Stop:")
                print(date)
                try:
                    idv = param['idv']
                    perFalse= "0"
                    hostbd.update_vodomatActivate(idv, perFalse)

                    reserve = {'reserve': 0}
                    get_reserve = hostbd.get_vodomat(idv)
                    reserve['reserve'] = get_reserve['reserve']
                    date['param'].update(reserve)
                    # tableSock[int(idv)].update({"locked": True})
                    bot.send_message(param['idT'], "Вы закрыли сеанс работы с водоматом, спасибо, что вы с нами")
                    send(date, idv)
                except:
                    bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")

            elif method == 'settings':
                print("Setting:")
                print(date)
                try:
                    idv = param['idv']
                    # tableSock[int(idv)].update({"locked": True})
                    bot.send_message(param['idT'], "Ваш запрос принят на смену настроект, ожидайте")
                    send(date, idv)
                    # tableSock[int(idv)].update({"locked": False})
                except:
                    bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")

            elif method == "AddUser":
                print("AddUser:")
                print(date)
                bot.send_message(date['param']['idT'], "Поздравляем, вы успешно прошли регистрацию и спасибо, что вы с нами и за ваш вклад, и подержку")
                userbd.add_user(date['param']['idT'], date['param']['name'])

            elif method == "PromoCode":
                print("PromoCode:")
                print(date)
                userbd.insert(date['param']['idT'], date['param']['inviter'])

            elif method == 'GetSettings':
                print("GetSettings:")
                print(date)

                try:
                    idv = param['idv']
                    date = hostbd.get_vodomat(idv)
                    print('date:')
                    print(date)
                    # tableSock[int(idv)].update({"locked": True})
                    bot.send_message(param['idT'], "Ваш запрос принят на получение настроект, ожидайте")
                    send(date, idv)
                    # tableSock[int(idv)].update({"locked": False})
                except:
                    bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")

            elif method == "Answer":

                print("Answer:")
                print(data)

                NewData = {'HowMuchWereSpent': '', 'HowMuchWere': '', 'HowMuchWereGiven': '', 'InfOfVodomat': ''}

                # счет пользоателя с БД
                ScoreOfUser = userbd.get_user(param['idT'])
                ScoreOfUser = int(ScoreOfUser['score'])


                # статус водомота с БД
                NewData['InfOfVodomat'] = hostbd.get_vodomatVVS(param['Status']['idv'])  # статус водомота с БД
                hostbd.delete_vodomatVVS(param['Status']['idv'])


                InfAboutOwnerAndVodomat = billing.SeekHowMuchScore(param, NewData, ScoreOfUser)
                admin = adminka.get_admin(param['Status']['idv'])
                InfAboutOwnerVodomat = userbd.get_user(admin['idT'])


                bill = billing.SeekSales(InfAboutOwnerAndVodomat, InfAboutOwnerVodomat)


                hostbd.update_vodomatScore(param['Status']['idv'], bill['InfOfVodomat'])
                bot.send_message(param['idT'], "У вас на счету %5.1f литров." % (param['score'] / 4))

                param['idv'] = 0
                print('hiiiiiii')


                userbd.update_user(**param)

                userbd.update_userAfterGotMoney(**bill['InfAboutOwnerVodomat'])


                for AdminUser in admin:
                    result = billing.percnt(InfAboutOwnerAndVodomat['HowMuchWereSpent'], AdminUser)
                    collect = {'idT': 0, 'idv': 0, 'score': 0}
                    collect['score'] = result
                    collect['idT'] = AdminUser['idT']
                    collect['idv'] = AdminUser['idv']
                    userfrombd = userbd.get_user(idT=AdminUser['idT'])
                    collect['score'] = collect['score'] + userfrombd['score']
                    userbd.update_user(**collect)


            elif method == "error":
                bot.send_message(param['idT'],
                                 "В ходе работы произошла ошибка, пожалуйста попробуйте еще разок, ладненько?")

            elif method == "status":  # for get information about hosts
                idv = param['idv']
                # global i
                prev = hostbd.get_vodomat2(idv)
                print("prev:")
                print(prev)
                print("param:")
                print(param)
                print('hey')
                if param['leftFromPaid'] != prev['leftFromPaid']:
                    hostbd.update_vodomat(**param)
                    print('1')
                    workbyfile.write_on_file(date)
                    i = 0
                    print('2')
                    # print("Savedate = %s" % date)
                else:
                   hostbd.update_vodomatTime(param['idv'])
                   print('outElse')
                   KnowAc = hostbd.get_vodomat(idv)
                   print("KnowAc:")
                   print(KnowAc)
                   if KnowAc['action'] == '1':
                       print('intoElse')
                       i = i + 1
                       print(i)
                       if i > 60:
                         print('intoIf')
                         user = userbd.get_userV(idv)
                         print('user:')
                         print(user)
                         ypar = {'method': 'Stop', 'param':{'idT': user['idT'], 'idv':user['idv']}}
                         print('ypar:')
                         print(ypar)
                         send(ypar,user['idv'])
                         i=0

                         idv = param['idv']
                         perFalse = "0"
                         hostbd.update_vodomatActivate(idv, perFalse)
                         # tableSock[int(idv)].update({"locked": True})


                         # Вывод кнопок
                         Get_points = types.ReplyKeyboardMarkup()
                         Get_points.row("Подключиться к водомату")
                         Get_points.row("Личный кабинет")
                         bot.send_message(user['idT'], "Вы закрыли сеанс работы с водоматом, спасибо, что вы с нами", reply_markup = Get_points)
                         user['idv'] = 0
                         userbd.update_useridv(**user)

            elif method == "connect":
                print("connect:")
                idv = param['idv']
                hostbd.add_host(idv)
                hostbd.update_vodomat(**param)
                # tableSock.update({date['param']['idv']: {"socket": sock, "locked": False}})
                tableSock.update({date['param']['idv']: {"socket": sock}})
                workbyfile.write_on_file(date)
                ypar = {'method': 'connect', 'param':'connection successfully'}
                send(ypar, idv)
            # else:
            #     idv = param['idv']
            #     ypar = {"method": "error", "param": {"type": "not method", "args": method}}
            #     send(ypar, idv)
        except ConnectionResetError:
            tableSock.pop({date['param']['idv']})
            print("Disconnect: ", addr)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(e)

# Соединение по двум портам
def conGateway():
    try:
        sock = socket.socket()
        sock.bind(('', 8080))
        return sock
    except:
        sock = socket.socket()
        sock.bind(('', 9090))
        return sock

# Наладка клинет-сервера
def habStart():
    sock = conGateway()
    sock.listen(1000)
    while True:
        print("hosthab")
        conn, addr = sock.accept()
        print("Connect: ", addr)
        t = threading.Thread(target=connect, args=(conn, addr))
        t.start()
habStart()
