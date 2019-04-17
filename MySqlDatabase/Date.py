import datetime

import pymysql

from MySqlDatabase import Seasons_and_Holidays


class DateObject:
    date_raw = None
    date = ''
    day_of_month = 0
    month_of_year = ''
    year = 0
    weekday = ''
    week_of_year = 0
    quarter = 0
    holiday = ''
    college_holidays = ''
    season = ''
    connection_remote = None
    weekday_number = -1
    month_name = ''



    def __init__(self, date_raw):
        self.date_raw = date_raw
        self.date = self.date_raw.strftime('%Y-%m-%d')

    def getKeyDate(self):
        return self.date

    def generateDateFields(self):
        self.day_of_month = self.date_raw.day
        self.month_of_year = self.date_raw.month
        self.year = self.date_raw.year
        self.weekday = self.date_raw.strftime('%A')
        self.week_of_year = self.date_raw.isocalendar()[1]
        self.quarter = (self.date_raw.month-1)//3 + 1
        self.season = Seasons_and_Holidays.get_season(self.date_raw)
        self.holiday = Seasons_and_Holidays.get_Holiday(self.date_raw)
        self.college_holidays = "Testing"
        self.weekday_number = self.date_raw.weekday()
        self.month_name = self.date_raw.strftime("%B")

    def generateInsertString(self):
        sql = 'INSERT INTO thesis.date(keyDate,DayOfMonth,MonthOfYear,Year,WeekOfYear,WeekDay,Quarter,Holiday,Season,CollegeHolidays,weekdayNumber,monthName)VALUES ' \
              '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        return sql

    def getDate(self,date_in):
        sql = "SELECT * FROM thesis.date where keyDate = %s;"
        cursor_local = self.connection_remote.cursor()
        cursor_local.execute(sql, date_in)
        for row in cursor_local:
            return row

    def generateTuple(self):
        return (self.date, self.day_of_month, self.month_of_year, self.year, self.week_of_year, self.weekday,
                self.quarter, self.holiday, self.season, self.college_holidays,self.weekday_number,self.month_name)

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

    def toString(self):
        print("Date Key: " + self.date)
        print("Day of Month: " + str(self.day_of_month))
        print("Month of Year: " + str(self.month_of_year))
        print("Year: " + str(self.year))
        print("Week of Year: " + str(self.week_of_year))
        print("Weekday: " + self.weekday)
        print("Quarter: " + str(self.quarter))
        print("Holiday: " + str(self.holiday))
        print("Season: " + self.season)
        print("College Holiday: " + self.college_holidays)
        pass



if __name__ == '__main__':
    print("Insert Date")
    date = None
    date_input = input('Date (now() or DD-MM-YYYY): ')
    if date_input == 'now()':
        date = datetime.datetime.today()
    else:
        date = datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
    obj = DateObject(date)
    obj.generateDateFields()
    obj.SQLOpen()
    obj.getDate(date.strftime('%Y-%m-%d'))
    # obj.insertIntoSQL()
    obj.SQLClose()
