import threading
import socket
import json
import telebot

token = "321273335:AAGC0-DP7Rwxu99_sN3sSVdYDOcPgu3869g"

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
                if hostWI['State'] == 'WAIT':
                        try:
                            userbd.update_user(**param)
                            hostbd.update_vodomatActivate(param['idv'], True)
                            idv = param['idv']
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
                    tableSock[int(idv)].update({"locked": True})
                    send(date, idv)
                except:
                    bot.send_message(param['idT'],
                                             "Приносим вам свои извинения,"
                                             "но водомат временно в не рабочем состоянии!")



            elif method == "Answer":
                idv=param['idv']
                tableSock[int(idv)].update({"locked": False})
                Status = data['Status']
                print("Answer:")
                print(date)
                #Score of user
                ScoreOfUser = userbd.get_user(param['idT'])
                TotalPaidBefore = int(ScoreOfUser['totalPaid'])
                TotalPaidAfter = Status['totalPaid']
                ScoreOfUser = int(ScoreOfUser['score'])
                HowMuchWereSpent = TotalPaidAfter - TotalPaidBefore #Сколько потратил
                HowMuchWere = HowMuchWereSpent + Status['leftfromPaid'] #Сколько было
                HowMuchWereGiven = HowMuchWere - ScoreOfUser

                # score of vodomat
                ScoreOfVodomat = hostbd.get_vodomat(param['idv'])
                ScoreOfVodomat = int(ScoreOfVodomat['score'])

                ScoreOfVodomat = ScoreOfVodomat - HowMuchWereGiven
                ScoreOfOwner = ScoreOfOwner + HowMuchWereSpent

                param['idv'] = 0
                userbd.update_user(**param)
                bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")

                print("ScoreOfVodomat:")
                print(ScoreOfVodomat)
                hostbd.update_vodomatScore(param['idv'], ScoreOfVodomat)
                hostbd.update_vodomatActivate(param['idv'], False)
                ypar = {'method': 'got', 'param': 'saved'}
                send(ypar, idv)

            elif method == "error":
                bot.send_message(param['idT'],
                                 "В ходе работы произошла ошибка, пожалуйста попробуйте еще разок, ладненько?")



            elif method == "status":  # for get information about hosts
                prev = hostbd.get_vodomat(param['idv'])
                idv = param['idv']
                ypar = {'method': 'got', 'param': 'saved'}
                if date != prev:
                    hostbd.update_vodomat(**param)
                    workbyfile.write_on_file(date)
                    # print("Savedate = %s" % date)
                send(ypar, idv)

            elif method == "connect":
                hostbd.add_host(param['idv'])
                idv = param['idv']
                hostbd.update_vodomat(**param)
                tableSock.update({date['param']['idv']: {"socket": sock, "locked": False}})
                workbyfile.write_on_file(date)
                ypar = {'method': 'got', 'param': 'saved'}
                send(ypar, idv)
            else:
                ypar = {"method": "error", "param": {"type": "not method", "args": method}}
                idv = param['idv']
                send(ypar, idv)



        except ConnectionResetError:
            tableSock.pop({date['param']['idv']})
            print("Disconnect: ", addr)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(e)

def habStart():
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1000)

    while True:
        print("hosthab")
        conn, addr = sock.accept()
        print("Connect: ", addr)
        t = threading.Thread(target=connect, args=(conn, addr))
        t.start()
habStart()
