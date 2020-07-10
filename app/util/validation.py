import re
from datetime import datetime


def validate_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_cpf(cpf):
    cpf = re.sub("[^0-9]", "", cpf)

    if len(cpf) != 11:
        return False

    if cpf == '11111111111' or \
        cpf == '22222222222' or \
        cpf == '33333333333' or \
        cpf == '44444444444' or \
        cpf == '55555555555' or \
        cpf == '66666666666' or \
        cpf == '77777777777' or \
        cpf == '88888888888' or \
        cpf == '99999999999':
            return False

    calc = lambda t: int(t[1]) * (t[0] + 2)
    d1 = (sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11
    d2 = (sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11

    if d1 == 10:
        d1 = 0
    if d2 == 10:
        d2 = 0
    if str(d1) == cpf[-2] and str(d2) == cpf[-1]:
        return True
    return False