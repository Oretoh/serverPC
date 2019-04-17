import pymysql
from datetime import datetime
import time
import json


from MySqlDatabase.Date import DateObject
from MySqlDatabase.Device import DeviceObject
from MySqlDatabase.Time import TimeObject


class ReadingObjectTemperature:

    
    reading_raw = None
    keyDate = None
    keyTime = None#
    keyDevice = None
    temp_value = -1
    date_input = ''
    device_input = ''



    def __init__(self, reading_raw):
        self.reading_raw = reading_raw
        self.set_fields()

    def set_fields(self):
        self.date_input = self.reading_raw['Time']
        self.device_input = self.reading_raw['id']
        self.temp_value = self.reading_raw['temp_value']
        
       
    def get_fields_reading(self):
        # class_input = 'Profissão, Ética e Sociedade'

        date = datetime.strptime(self.date_input, '%Y-%m-%dT%H:%M:%S.%f+00:00')

        self.date_engine(date)
        self.time_engine(date)
        self.device_engine(self.device_input)

    def date_engine(self, date):
        date_obj = DateObject(date)
        date_obj.generateDateFields()
        self.keyDate = date_obj.getKeyDate()
     
    def time_engine(self, date):
        time_obj = TimeObject(date)
        time_obj.generateTimeField()
        self.keyTime = time_obj.getKeyTime()#

    def device_engine(self, device_input):
        device_obj = DeviceObject(device_input)
        device_obj.SQLOpen()
        row_data = device_obj.get_device(device_obj.getDeviceKey())
        if row_data is None:
            print("Device does not exist please use file CreateDevice.py to create a new device",flush=True)
        else:
            self.keyDevice = row_data['keyDevice']
        device_obj.SQLClose()


    @staticmethod
    def generate_insert_string():
        sql = 'INSERT INTO thesis.reading_temperature(keyDate, keyTime, keyDevice, temp_value)' \
              'VALUES(%s,%s,%s,%s);'
        return sql
    
    

    def generate_tuple(self):
        return self.keyDate, self.keyTime, self.keyDevice, self.temp_value

    
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
        except:
            result = cursor_local
            print(result)
            raise

    def sql_close(self):
        self.connection_remote.close()
