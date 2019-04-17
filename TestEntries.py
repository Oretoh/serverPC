# {"id":"avac_aud1","kW":5, "current":3}
# {"id":"avac_aud2","kW":3, "current":1.5}
# {"id":"light_aud1","kW":2, "current":1.3}
# {"id":"light_aud2","kW":3, "current":1.4}
# {"id":"total_light_other_aud1_aud2","kW":10, "current":9}
import datetime
import json
import random
import time

from FlaskWebServer import process_Reading_data
from MySqlDatabase.Reading import ReadingObject
from ReadingIncomplete import ReadingIncomplete

ids = ['avac_aud1',
       'avac_aud2',
       'light_aud1',
       'light_aud2',
       'total_light_other_aud1_aud2']
date_time = datetime.datetime.now()
incomplete_objects_data = []
light1 = 0
light2 = 0

def start():
    global date_time
    global incomplete_objects_data
    global ids

    dates = 0

    with open('IncompleteObjects.json') as f:
        data = json.load(f)
        for objects in data:
            incomplete_objects_data.append(ReadingIncomplete(objects))
    f.close()



    while dates < 2976:
        date_time = date_time + datetime.timedelta(minutes=30)
        date_time_string = date_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        dates = dates + 1
        temp = random.uniform(10, 30)
        for id in ids:
            kW = define_kW(id)
            current = 0
            if kW == 0:
                current = 0
            else:
                random.uniform(1.2, 30)
            entry = {"Internal" : 0,
                    "Time": date_time_string,
                     "id": id,
                     "kW": kW,
                     "current": current}
            process_reading_data(entry, temp)
            process_incomplete(id, kW, temp, date_time_string)



def process_incomplete(id_d, kW, temp,time_d):
    for obj in incomplete_objects_data:
        if obj.check_if_field_exists(id_d):
            obj.set_field_value(id_d, kW)
            if obj.check_ready_to_send():
                return_string = obj.create_send_string(time_d)
                reading = ReadingObject(return_string, temp, Interval=3600)
                reading.get_fields_reading()
                reading.sql_open()
                reading.insert_into_sql()
                reading.sql_close()
                obj.reset_values(-1)

def process_reading_data(entry, temp):
    reading = ReadingObject(entry, temp)
    reading.get_fields_reading()
    reading.sql_open()
    reading.insert_into_sql()
    reading.sql_close()


def define_kW(id):
    global light1
    global light2

    rando = random.randint(0, 1)
    if id == 'avac_aud1' or id == 'avac_aud2':
        if rando == 0:
            return 0
        else:
            return random.uniform(1.2, 2)

    elif id == 'light_aud1':
        if rando == 0:
            return 0
        else:
            light = random.uniform(1, 1.5)
            light1 = light
            return light

    elif id == 'light_aud2':
        if rando == 0:
            return 0
        else:
            light = random.uniform(1, 1.5)
            light2 = light
            return light

    elif id == 'total_light_other_aud1_aud2':
        if rando == 0:
            other = 0
            return other + light1 + light2
        else:
            other = random.uniform(0.5, 4)
            return other + light1 + light2


def test_kwh():
    notion = 1400
    value = 0
    timel = 0
    go = True
    kWh = 0
    while go:
        value = value + notion/5
        timel = timel + 1
        if timel % 900 == 0:
            print('kW: '+str(value / 1000))
            kWh = kWh + value / (1000*720)
            print('kWH: '+str(kWh))
            print(str(value))
            print('Hour expected: '+str((value / (1000*4600/5))*4))
            value = 0
            if timel >= 892800:
                go = False

test_kwh()