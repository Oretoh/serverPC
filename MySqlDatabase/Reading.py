import pymysql
from datetime import datetime
import time
import json

from MySqlDatabase.Class import ClassObject
from MySqlDatabase.Date import DateObject
from MySqlDatabase.Device import DeviceObject
from MySqlDatabase.Time import TimeObject


class ReadingObject:
    INTERVAL = 60
    DATA_READ_CYCLE = 10
    
    reading_raw = None
    keyDate = None
    keyTime = None#
    keyClassName = None
    keyDevice = None
    kW = -1
    kWh = -1
    Temp = -1
    current = -1
    date_input = ''
    device_input = ''
    seconds = ''
    millis = ''
    seq = None
    alert = []


    def __init__(self, reading_raw, temperature, Interval):
        self.Temp = temperature
        self.reading_raw = reading_raw
        self.INTERVAL = Interval
        self.set_fields()

    def set_fields(self):
        self.date_input = self.reading_raw['Time']
        self.alert = self.reading_raw['alert']
        if self.reading_raw['Internal'] == 1:
            self.device_input = self.reading_raw['id']
            self.kW = self.reading_raw['kW']
            self.kWh = self.kW / self.INTERVAL
            self.current = None
            self.seq = None
        else:
            self.device_input = self.reading_raw['id']
            self.kW = self.reading_raw['kW']
            self.kWh = self.kW / self.INTERVAL
            self.current = (( self.reading_raw['kW'] / 240) * 1000) / self.DATA_READ_CYCLE
            self.seq = self.reading_raw['seq']

    def get_fields_reading(self):
        # class_input = 'Profissão, Ética e Sociedade'

        date = datetime.strptime(self.date_input, '%Y-%m-%dT%H:%M:%S.%f+00:00')

        self.date_engine(date)
        self.time_engine(date)
        self.device_engine(self.device_input)

        # self.class_engine(class_input)

        # print(self.keyDate)
        # print(self.keyTime)
        # print(self.keyDevice)
        # print(self.keyClassName)

    def date_engine(self, date):
        date_obj = DateObject(date)
        date_obj.SQLOpen()
        row_data = date_obj.getDate(date_obj.getKeyDate())
        if row_data is None:
            date_obj.generateDateFields()
            date_obj.insertIntoSQL()
            self.keyDate = date_obj.getKeyDate()
        else:
            self.keyDate = row_data['keyDate'].strftime('%Y-%m-%d')
        date_obj.SQLClose()

    def time_engine(self, date):
        self.seconds = date.strftime('%S')
        self.millis = date.strftime('%f')
        
        minute_correction = int(date.strftime('%M'))
        if minute_correction % 10 != 0:
            delay = minute_correction % 10
            minute_correction = minute_correction - delay
            self.alert.append(("Delay",delay))
           
        date = date.replace(minute = minute_correction)   
        print(date,flush=True)
        time_obj = TimeObject(date)
        time_obj.SQLOpen()
        row_data = time_obj.getTime(time_obj.getKeyTime())
        if row_data is None:
            # generates fields and inserts them into MySQL
            time_obj.generateTimeField()
            time_obj.insertIntoSQL()
            self.keyTime = time_obj.getKeyTime()
        else:
            # Converts time delta into hour:minute
            timedelta = row_data['keyTime']
            self.keyTime = (datetime.min + timedelta).time().strftime('%H:%M:00')
        time_obj.SQLClose()

    def device_engine(self, device_input):
        device_obj = DeviceObject(device_input)
        device_obj.SQLOpen()
        row_data = device_obj.get_device(device_obj.getDeviceKey())
        if row_data is None:
            print("Device does not exist please use file CreateDevice.py to create a new device",flush=True)
        else:
            self.keyDevice = row_data['keyDevice']
        device_obj.SQLClose()

#
    # def class_engine(self, class_input):
    #     class_obj = ClassObject(class_input)
    #     class_obj.sql_open()
    #     row_data = class_obj.get_class(class_obj.get_class_key())
    #     if row_data is None:
    #         print("Class does not exist please use file CreateDevice.py to create a new device")
    #     else:
    #         self.keyClassName = row_data['ClassName']
    #         class_obj.sql_close()


    @staticmethod
    def generate_insert_string():
        sql = 'INSERT INTO thesis.reading(Seq,keyDate, keyTime, keyClassName, keyDevice, Current, kWh, kW, Temp,Secs,Millis)' \
              'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        return sql
    
    @staticmethod
    def generate_insert_alert_string():
        sql = 'INSERT INTO thesis.alert(keyDate, keyTime, keyDevice,Description,Value)' \
              'VALUES(%s,%s,%s,%s,%s);'
        return sql

    def generate_tuple(self):
        return self.seq, self.keyDate, self.keyTime, self.keyClassName, self.keyDevice, self.current, self.kWh, self.kW, self.Temp, self.seconds, self.millis

    def generate_alert_tuple(self,one_alert,value_alert):
        return self.keyDate, self.keyTime, self.keyDevice, one_alert,str(value_alert)
    
    def sql_open(self):
        self.connection_remote = pymysql.connect(
            host="127.0.0.1",
            user="admin",
            passwd="lisonco20",
            database="thesis",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True)

    def insert_into_sql(self):
        cursor_local = self.connection_remote.cursor()
        try:
            cursor_local.execute(self.generate_insert_string(), self.generate_tuple())
            if len(self.alert) != 0:
                for alert_one in self.alert:
                    cursor_local.execute(self.generate_insert_alert_string(), self.generate_alert_tuple(alert_one[0],alert_one[1]))
            self.alert = []
        except:
            result = cursor_local
            print(result)
            raise

    def sql_close(self):
        self.connection_remote.close()


if __name__ == '__main__':
    # start = time.time()
    # str = {"Internal": 0, "Time":"2018-12-04T22:32:46.587733+00:00",{"id":"avac_aud1","kW":10, "current":222}
    obj = ReadingObject(str, 40)
    obj.get_fields_reading()
    obj.sql_open()
    obj.insert_into_sql()
    obj.sql_close()
    # print(time.time() - start)

    # paylo