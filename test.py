from Archive import userbd

# data = {'InfAboutOwnerVodomat':'', 'InfOfVodomat':''}
# InfAboutOwnerVodomat = {'consumerPump': 0, 'tumperDoor': 0, 'contVolume': 0}
# print(InfAboutOwnerVodomat)
# data['InfAboutOwnerVodomat'] = InfAboutOwnerVodomat
# #
# InfOfVodomat = {'Voltage': 0, 'vs.freeButton': 1, 'currentContainerVolume': '9505', 'idv': 3, 'billAccept': 0, 'input10Counter': 0, 'mainPump': 0}
# data['InfOfVodomat'] = InfOfVodomat
# print(data)
# InfAboutOwnerVodomat = {'idv': 3, 'billAccept': 0, 'input10Counter': 0, 'mainPump': 0}
ScoreOfUser = userbd.get_user(167315364)  # счет пользоателя с БД
ScoreOfUser = int(ScoreOfUser['score'])
# aaaa = {'InfAboutOwner':''}
# aaaa['InfAboutOwner'] = InfAboutOwnerVodomat
# data.update(aaaa)
# print(data)
# idv = int(param['Status']['idv'])
# # tableSock[int(idv)].update({"locked": False})
#
# #статус водоматы с водомата
# StatusVodomataFromVodomat = date['param']['Status']
# print("StatusVodomataFromVodomat:")
# print(StatusVodomataFromVodomat)
#
# #счет пользоателя с БД
# #Score of user
# ScoreOfUser = userbd.get_user(param['idT'])
#
# ScoreOfUser = int(ScoreOfUser['score'])
# print("ScoreOfUser:")
# print(ScoreOfUser)
#
# #статус водомота с БД
# StatusVodomataFromDB = hostbd.get_vodomatVVS(idv)
# print("StatusVodomataFromDB:")
# print(StatusVodomataFromDB)
#
# #затраты до
# TotalPaidBefore = int(StatusVodomataFromDB['totalPaid'])
# print("TotalPaidBefore:")
# print(TotalPaidBefore)
#
# #затраты после
# TotalPaidAfter = StatusVodomataFromVodomat['totalPaid']
# print("TotalPaidAfter:5")
# print(TotalPaidAfter)
#
# # Сколько потратил
# HowMuchWereSpent = TotalPaidAfter - TotalPaidBefore
# print("HowMuchWereSpent:")
# print(HowMuchWereSpent)
#
# # Сколько было
# HowMuchWere = HowMuchWereSpent + StatusVodomataFromVodomat['leftFromPaid']
# print("HowMuchWere:")
# print(HowMuchWere)
#
# # Сколько он закинул на счет
# HowMuchWereGiven = HowMuchWere - ScoreOfUser
# print("HowMuchWereGiven:")
# print(HowMuchWereGiven)
#
# # Информация водомата с БД
# # InfOfVodomat = hostbd.get_vodomat(idv)
# InfOfVodomat = StatusVodomataFromDB
# hostbd.delete_vodomatVVS(idv)
# print("InfOfVodomat:")
# print(InfOfVodomat)
#
# print("InfOfVodomat['sale']:")
# print(InfOfVodomat['sale'])
#
# print("InfOfVodomat['сashing']:")
# print(InfOfVodomat.get('сashing'))
#
# admin = adminka.get_admin(idv)
# print('admin:')
# print(admin)
#
# InfAboutOwnerVodomat = userbd.get_user(admin['idT'])
# print('InfAboutOwnerVodomat:')
# print(InfAboutOwnerVodomat)
#
# # Наличка водомата с БД
#
# try:
#     InfOfVodomat['сashing'] = int(InfOfVodomat.get('сashing')) + int(HowMuchWereGiven)
#     InfAboutOwnerVodomat['сashing'] = InfAboutOwnerVodomat['сashing'] + HowMuchWereGiven
# except:
#     InfOfVodomat['сashing'] = 0
#     InfAboutOwnerVodomat['сashing']=0
#
# print("InfOfVodomat['сashing']:")
# print(InfOfVodomat.get('сashing'))
#
# print("InfAboutOwnerVodomat['сashing']:")
# print(InfAboutOwnerVodomat['сashing'])
#
# # Кредит водомата с БД
# # credit = int(InfOfVodomat['credit'])
# print("InfOfVodomat['credit']:")
# print(InfOfVodomat['credit'])
#
# credit = HowMuchWereGiven - HowMuchWereSpent
# if credit > 0:
#     InfOfVodomat['credit'] = InfOfVodomat['credit'] + credit
#     print("InfOfVodomat['credit']:")
#     print(InfOfVodomat['credit'])
#
#     InfAboutOwnerVodomat['credit'] = InfAboutOwnerVodomat['credit'] + credit
#     print("InfAboutOwnerVodomat['credit']:")
#     print(InfAboutOwnerVodomat['credit'])
# else:
#     credit = 0
# print("InfOfVodomat['credit']:")
# print(InfOfVodomat['credit'])
#
#
# # Продажи водомата с БД
# print("InfOfVodomat['sale']:")
# print(InfOfVodomat['sale'])
#
# InfOfVodomat['sale'] = InfOfVodomat['sale'] + HowMuchWereSpent
# print("InfOfVodomat['sale']:")
# print(InfOfVodomat['sale'])
#
# InfAboutOwnerVodomat['sale'] = InfAboutOwnerVodomat['sale'] + HowMuchWereSpent
# print('InfAboutOwnerVodomat[sale]:')
# print(InfAboutOwnerVodomat['sale'])


# bot.send_message(param['idT'], "У вас на счету " + str(param['score']) + "₽")
#
# ypar = {'method': 'got', 'param': 'saved'}
# send(ypar, idv)