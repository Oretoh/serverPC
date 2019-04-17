import pymysql
from datetime import datetime, time

from MySqlDatabase.Date import DateObject


class TimeObject:
    time_raw = None
    timeP = ''
    hour = ''
    min = ''
    period = ''


    def __init__(self, time_raw):
        self.time_raw = time_raw
        self.timeP = self.time_raw.strftime('%H:%M:00')

    def getKeyTime(self):
        return self.timeP

    def generateTimeField(self):
        self.hour = self.time_raw.strftime('%H')
        self.min = self.time_raw.strftime('%M')
        self.period = self.getPeriodOfDay()


    def getPeriodOfDay(self):
        hour_calculate = int(self.hour)
        min_calculate = int(self.min)
        if self.is_time_between(time(6, 0), time(11, 59), time(hour_calculate, min_calculate)):
            return "Morning"
        if self.is_time_between(time(12, 0), time(17, 59), time(hour_calculate, min_calculate)):
            return "Afternoon"
        if self.is_time_between(time(18, 0), time(00, 59), time(hour_calculate, min_calculate)):
            return "Night"
        if self.is_time_between(time(1, 0), time(5, 59), time(hour_calculate, min_calculate)):
            return "Early Morning"


    def is_time_between(self, begin_time, end_time, check_time):
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else:  # crosses midnight
            return check_time >= begin_time or check_time <= end_time

    def toString(self):
        print("Key: "+self.timeP)
        print("Hour: " + self.hour)
        print("Minute: " + self.min)
        print("Period Of Time: " + self.period)

    def generateInsertString(self):
        sql = 'INSERT INTO thesis.time(keyTime,Hour,Minute,PeriodOfTime)VALUES ' \
              '(%s,%s,%s,%s);'
        return sql

    def getTime(self, time_in):
        sql = "SELECT * FROM thesis.time where keyTime = %s;"
        cursor_local = self.connection_remote.cursor()
        cursor_local.execute(sql, time_in)
        for row in cursor_local:
            return row

    def generateTuple(self):
        return (self.timeP, self.hour, self.min, self.period)

    def SQLOpen(self):
        self.connection_remote = pymysql.connect(
            host="127.0.0.1",
            user="admin",
            passwd="lisonco20",
            database="thesis",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True)

    def insertIntoSQL(self):
        cursor_local = self.connection_remote.cursor()
        cursor_local.execute(self.generateInsertString(), self.generateTuple())

    def SQLClose(self):
        self.connection_remote.close()

if __name__ == '__main__':
    print("Insert Date and Time")
    date = None
    date_input = input('Date (now() or DD-MM-YYYY HH:MM:SS): ')
    if date_input == 'now()':
        date = datetime.today()
    else:
        date = datetime.strptime(date_input, '%d-%m-%Y %H:%M:%S')

    obj = DateObject(date)
    obj.generateDateFields()
    obj.SQLOpen()
    obj.insertIntoSQL()
    obj.getDate(date.strftime('%Y-%m-%d'))
    obj.SQLClose()

    obj = TimeObject(date)
    obj.generateTimeField()
    obj.SQLOpen()
    obj.insertIntoSQL()
    obj.getTime(date.strftime('%H:%M'))
    obj.SQLClose()
