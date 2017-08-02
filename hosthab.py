import threading
import socket
import json
import telebot

file = open("/opt/key.json")

text = file.read()

config = json.loads(text)

token = config["token"]

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
    print(tableSock[int(idv)]["locked"])
    if data['method'] == 'got' and tableSock[int(idv)]["locked"] == False:
        data = cod(data)
        tableSock[int(idv)]["socket"].send(data)
    else:
        if data['method'] == 'Start' or data['method'] == 'Stop' or data['method'] == 'settings':
            data = cod(data)
            tableSock[int(idv)]["socket"].send(data)
    print("end send")


def connect(sock, addr):
    while True:
        data = sock.recv(2048)
        data = data.decode("utf-8")


        if data is None:
            print("Disconnect. Not Data: ", addr)
            return False

        date = json.loads(data)
        try:
            method = date.get("method")
            param = date.get("param")


            if method == "Start":
                print("Activate:")
                print(date)

                hostWI = hostbd.get_vodomat(int(param['idv']))
                print('hostWI:')
                print(hostWI)
                if hostWI['State'] == 'WAIT':
                        print('Hi')
                        try:
                            userbd.update_user(**param)
                            perTrue = "1"
                            idv = param['idv']
                            hostbd.update_vodomatActivate(idv, perTrue)
                            tableSock[int(idv)].update({"locked": True})
                            send(date, idv)
                        except:
                            bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")

            elif method == "Stop":
                print("Stop:")
                print(date)
                try:
                    idv = param['idv']
                    perFalse= "0"
                    hostbd.update_vodomatActivate(idv, perFalse)
                    tableSock[int(idv)].update({"locked": True})
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
                    tableSock[int(idv)].update({"locked": True})
                    send(date, idv)
                    tableSock[int(idv)].update({"locked": False})
                except:
                    bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")

            elif method == 'GetSettings':
                print("GetSettings:")
                print(date)

                try:
                    idv = param['idv']
                    date = hostbd.get_vodomat(idv)
                    print('date:')
                    print(date)
                    tableSock[int(idv)].update({"locked": True})
                    send(date, idv)
                    tableSock[int(idv)].update({"locked": False})
                except:
                    bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")

            elif method == "Answer":

                print("Answer:")
                print(date)

                idv = int(param['idv'])
                tableSock[int(idv)].update({"locked": False})

                #статус водоматы с водомата
                StatusVodomataFromVodomat = date['Status']
                print("StatusVodomataFromVodomat:")
                print(StatusVodomataFromVodomat)

                #счет пользоателя с БД
                #Score of user
                ScoreOfUser = userbd.get_user(param['idT'])
                print("ScoreOfUser:2")
                print(ScoreOfUser)
                ScoreOfUser = int(ScoreOfUser['score'])
                print("ScoreOfUser:6")
                print(ScoreOfUser)

                #статус водомота с БД
                StatusVodomataFromDB = hostbd.get_vodomat(idv)
                print("SostoyanieVodomata:3")
                print(StatusVodomataFromDB)

                #затраты до
                TotalPaidBefore = int(StatusVodomataFromDB['totalPaid'])
                print("TotalPaidBefore:4")
                print(TotalPaidBefore)

                #затраты после
                TotalPaidAfter = StatusVodomataFromVodomat['totalPaid']
                print("TotalPaidAfter:5")
                print(TotalPaidAfter)

                # Сколько потратил
                HowMuchWereSpent = TotalPaidAfter - TotalPaidBefore
                print("HowMuchWereSpent:")
                print(HowMuchWereSpent)

                # Сколько было
                HowMuchWere = HowMuchWereSpent + StatusVodomataFromVodomat['leftFromPaid']
                print("HowMuchWere:")
                print(HowMuchWere)

                # Сколько он закинул на счет
                HowMuchWereGiven = HowMuchWere - ScoreOfUser
                print("HowMuchWereGiven:")
                print(HowMuchWereGiven)

                # Информация водомата с БД
                InfOfVodomat = hostbd.get_vodomat(idv)
                print("InfOfVodomat:")
                print(InfOfVodomat)

                print("InfOfVodomat['sale']:")
                print(InfOfVodomat['sale'])

                print("InfOfVodomat['сashing']:")
                print(InfOfVodomat.get('сashing'))

                admin = adminka.get_admin(idv)
                print('admin:')
                print(admin)

                InfAboutOwnerVodomat = userbd.get_user(admin['idT'])
                print('InfAboutOwnerVodomat:')
                print(InfAboutOwnerVodomat)

                # Наличка водомата с БД

                try:
                    InfOfVodomat['сashing'] = int(InfOfVodomat.get('сashing')) + int(HowMuchWereGiven)
                    InfAboutOwnerVodomat['сashing'] = InfAboutOwnerVodomat['сashing'] + HowMuchWereGiven
                except:
                    InfOfVodomat['сashing'] = 0
                    InfAboutOwnerVodomat['сashing']=0

                print("InfOfVodomat['сashing']:")
                print(InfOfVodomat.get('сashing'))

                print("InfAboutOwnerVodomat['сashing']:")
                print(InfAboutOwnerVodomat['сashing'])

                # Кредит водомата с БД
                # credit = int(InfOfVodomat['credit'])
                print("InfOfVodomat['credit']:")
                print(InfOfVodomat['credit'])

                credit = HowMuchWereGiven - HowMuchWereSpent
                if credit > 0:
                    InfOfVodomat['credit'] = InfOfVodomat['credit'] + credit
                    print("InfOfVodomat['credit']:")
                    print(InfOfVodomat['credit'])

                    InfAboutOwnerVodomat['credit'] = InfAboutOwnerVodomat['credit'] + credit
                    print("InfAboutOwnerVodomat['credit']:")
                    print(InfAboutOwnerVodomat['credit'])
                else:
                    credit = 0
                print("InfOfVodomat['credit']:")
                print(InfOfVodomat['credit'])


                # Продажи водомата с БД
                print("InfOfVodomat['sale']:")
                print(InfOfVodomat['sale'])

                InfOfVodomat['sale'] = InfOfVodomat['sale'] + HowMuchWereSpent
                print("InfOfVodomat['sale']:")
                print(InfOfVodomat['sale'])

                InfAboutOwnerVodomat['sale'] = InfAboutOwnerVodomat['sale'] + HowMuchWereSpent
                print('InfAboutOwnerVodomat[sale]:')
                print(InfAboutOwnerVodomat['sale'])

                bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")

                hostbd.update_vodomatScore(idv, InfOfVodomat)

                param['idv'] = 0
                print('hiiiiiii')
                userbd.update_user(**param)

                userbd.update_userAfterGotMoney(**InfAboutOwnerVodomat)

                ypar = {'method': 'got', 'param': 'saved'}
                send(ypar, idv)


            elif method == "error":
                idv = param['idv']
                bot.send_message(param['idT'],
                                 "В ходе работы произошла ошибка, пожалуйста попробуйте еще разок, ладненько?")
                ypar = {'method': 'got', 'param': 'saved'}
                send(ypar, idv)

            elif method == "status":  # for get information about hosts
                idv = param['idv']
                prev = hostbd.get_vodomat(idv)
                ypar = {'method': 'got', 'param': 'saved'}
                if date != prev:
                    hostbd.update_vodomat(**param)
                    workbyfile.write_on_file(date)
                    # print("Savedate = %s" % date)
                send(ypar, idv)

            elif method == "connect":
                idv = param['idv']
                hostbd.add_host(idv)
                hostbd.update_vodomat(**param)
                tableSock.update({date['param']['idv']: {"socket": sock, "locked": False}})
                workbyfile.write_on_file(date)
                ypar = {'method': 'got', 'param': 'saved'}
                send(ypar, idv)
            else:
                idv = param['idv']
                ypar = {"method": "error", "param": {"type": "not method", "args": method}}
                send(ypar, idv)
        except ConnectionResetError:
            tableSock.pop({date['param']['idv']})
            print("Disconnect: ", addr)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(e)

def conGateway():
    try:
        sock = socket.socket()
        sock.bind(('', 8080))
        return sock
    except:
        sock = socket.socket()
        sock.bind(('', 9090))
        return sock

def habStart():
    sock = conGateway()
    # sock.bind(('', 9090))
    sock.listen(1000)
    while True:
        print("hosthab")
        conn, addr = sock.accept()
        print("Connect: ", addr)
        t = threading.Thread(target=connect, args=(conn, addr))
        t.start()
habStart()
