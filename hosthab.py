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
        if data['method'] == 'Start' or data['method'] == 'Stop':
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

            elif method == "Answer":

                print("Answer:")
                print(date)

                idv = param['idv']
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

                # Наличка водомата с БД
                # cashing = int(InfOfVodomat['сashing'])
                # print("сashing:")
                # print(cashing)
                # cashing = cashing + HowMuchWereGiven
                InfOfVodomat['сashing']= InfOfVodomat['сashing'] + HowMuchWereGiven
                print("InfOfVodomat['сashing']:")
                print(InfOfVodomat['сashing'])


                # Кредит водомата с БД
                # credit = int(InfOfVodomat['credit'])
                print("InfOfVodomat['credit']:")
                print(InfOfVodomat['credit'])

                credit = HowMuchWereGiven - HowMuchWereSpent
                if credit > 0:
                    InfOfVodomat['credit'] = InfOfVodomat['credit'] + credit
                    print("InfOfVodomat['credit']:")
                    print(InfOfVodomat['credit'])
                print("InfOfVodomat['credit']:")
                print(InfOfVodomat['credit'])


                # Продажи водомата с БД
                # sale = int(InfOfVodomat['sale'])
                print("InfOfVodomat['sale']:")
                print(InfOfVodomat['sale'])

                InfOfVodomat['sale'] = InfOfVodomat['sale'] + HowMuchWereSpent
                print("InfOfVodomat['sale']:")
                print(InfOfVodomat['sale'])

                # ScoreOfVodomat = ScoreOfVodomat - HowMuchWereGiven
                # ScoreOfOwner=50
                # ScoreOfOwner = ScoreOfOwner + HowMuchWereSpent

                bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")

                hostbd.update_vodomatScore(idv, InfOfVodomat)


                param['idv'] = 0

                userbd.update_user(**param)

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
        sock.bind(('', 9090))
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
