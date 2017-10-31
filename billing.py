

# Сколько потратил
def HowMuchSpent(TotalPaidAfter, TotalPaidBefore): # Сколько потратил
    HowMuchWereSpent = TotalPaidAfter - TotalPaidBefore
    return HowMuchWereSpent

# Сколько было
def HowMuchWereU(HowMuchWereSpent, leftFromPaid): # Сколько было
    HowMuchWere = HowMuchWereSpent + leftFromPaid
    return HowMuchWere

# Сколько он закинул на счет
def HowMuchWereUp(HowMuchWere, ScoreOfUser):
    HowMuchWereGiven = HowMuchWere - ScoreOfUser # Сколько он закинул на счет
    return HowMuchWereGiven

def SeekHowMuchScore(param, data, ScoreOfUser):



    # статус водоматы с водомата
    StatusVodomataFromVodomat = param['Status']

    # затраты до
    TotalPaidBefore = int(data['InfOfVodomat']['totalPaid'])     # затраты до

    # затраты после
    TotalPaidAfter = StatusVodomataFromVodomat['totalPaid']     # затраты после




    # Сколько потратил
    data['HowMuchWereSpent'] = HowMuchSpent(TotalPaidAfter, TotalPaidBefore)   # Сколько потратил

    # Сколько было
    data['HowMuchWere'] = HowMuchWereU(data['HowMuchWereSpent'], StatusVodomataFromVodomat['leftFromPaid'])    # Сколько было

    # Сколько он закинул на счет
    data['HowMuchWereGiven'] = HowMuchWereUp(data['HowMuchWere'], ScoreOfUser)    # Сколько он закинул на счет

    return data





def SeekSales(data, InfAboutOwnerVodomat):
    # Наличка
    try:
        data['InfOfVodomat']['сashing'] = data['InfOfVodomat']['сashing'] + data['HowMuchWereGiven']
        InfAboutOwnerVodomat['сashing'] = InfAboutOwnerVodomat['сashing'] + data['HowMuchWereGiven']
    except:
        data['InfOfVodomat']['сashing'] = 0
        InfAboutOwnerVodomat['сashing'] = 0

    # Кредит
    credit = data['HowMuchWereGiven'] - data['HowMuchWereSpent']
    if credit > 0:
        data['InfOfVodomat']['credit'] = data['InfOfVodomat']['credit'] + credit
        InfAboutOwnerVodomat['credit'] = InfAboutOwnerVodomat['credit'] + credit
    else:
        credit = 0

    # Продажа
    data['InfOfVodomat']['sale'] = data['InfOfVodomat']['sale'] + data['HowMuchWereSpent']
    InfAboutOwnerVodomat['sale'] = InfAboutOwnerVodomat['sale'] + data['HowMuchWereSpent']

    perem = {'InfAboutOwnerVodomat':''}
    perem['InfAboutOwnerVodomat'] = InfAboutOwnerVodomat

    data.update(perem)

    return data


def percnt(HowMuchWereGiven, AdminUser):
    result = HowMuchWereGiven * (AdminUser['percent'] / 100)
    return result