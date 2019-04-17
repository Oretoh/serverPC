#!/usr/bin/env python
from datetime import date, datetime

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('Winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('Sprint', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('Summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('Autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('Winter', (date(Y, 12, 21),  date(Y, 12, 31)))]

def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)


holiday_list = [
    ("01-01", "Ano Novo"),
    ("30-03", "Sexta-feira Santa"),
    ("25-04", "Dia da Liberdade"),
    ("01-05", "Dia Trabalhador"),
    ("31-05", "Corpo Deus"),
    ("10-06", "Dia Portugal"),
    ("15-07", "Assunção de Nossa Senhora"),
    ("05-10", "Implatação da Republica"),
    ("01-11", "Dia de Todos os Santos"),
    ("01-12", "Restauração da Independncia"),
    ("08-12", "Dia da Imaculada Conceicao"),
    ("25-12", "Natal")

]
def get_Holiday(date):
    holiday = None
    day_format = date.strftime('%d') + "-" + date.strftime('%m')
    if day_format == calc_easter(date.year):
        holiday = "Easter"
    else:
        for hol in holiday_list:
                if day_format == hol[0]:
                    holiday = hol[1]
    return holiday

def calc_easter(year):
    "Returns Easter as a date object."
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    date_easter = date(year, month, day)
    return date_easter.strftime('%d') + "-" + date_easter.strftime('%m')
