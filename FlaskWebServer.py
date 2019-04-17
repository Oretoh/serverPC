import threading
from pprint import pprint


import gc

import sys#

import datetime
import requests
import time
from flask import Flask, request, jsonify
import json
import pyowm
import pymysql

from Correction.CorrectionAlgorithm import CorrectionAlgorithm
from MySqlDatabase.Reading import ReadingObject
from MySqlDatabase.Reading_Temperature import ReadingObjectTemperature
from MySqlDatabase.SensorData import SensorDataObject
from ReadingIncomplete import ReadingIncomplete

app = Flask(__name__)
owm = pyowm.OWM('daa8ea25a8ef817b9e2a10d4569fa27f')
incomplete_objects_data = []
temp = -1
#
#

time_latest_entry = None#
corrector = None
corrective_measure = False
devices = {}
last_entry_dict = {}
margin_devices = {}

DATA_INTERVAL = 10
timer_running = False


@app.before_first_request
def start():
    def initialize_web_server():
        global corrector
        global tracker 
        corrector = CorrectionAlgorithm('1')
        get_objects_data()
        get_devices()
        get_Temp_loop()

    def get_objects_data():
        global incomplete_objects_data
        with open('IncompleteObjects.json') as f:
            data = json.load(f)
            for objects in data:
                incomplete_objects_data.append(ReadingIncomplete(objects))
        f.close()

    def get_Temp_loop():
        global temp#
        global owm
        while True:
            try:
                observation_list = owm.weather_at_coords(38.74868698676801, -9.155080982973573)
                temp = observation_list.get_weather().get_temperature('celsius')['temp']
                time.sleep(1800)
            except:
                temp_loop_error()

    def temp_loop_error():
        global temp
        error = True#
        while error:
            try:
                observation_list = owm.weather_at_coords(38.74868698676801, -9.155080982973573)
                temp = observation_list.get_weather().get_temperature('celsius')['temp']
                error = False
            except:
                temp = -1
            time.sleep(5)#

    def get_devices():
        global devices#
        connection_remote = pymysql.connect(
            host="127.0.0.1",
            user="admin",
            passwd="lisonco20",
            database="thesis",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True)
        sql = "SELECT * FROM thesis.device where Active = 1;"
        cursor_local = connection_remote.cursor()
        cursor_local.execute(sql)
        for row in cursor_local:
            devices[row["devEui"]] = {'kd': row['keyDevice'], 'dt': row['DevType']}
            last_entry_dict[row['keyDevice']] = {'sequence': -1, 'kW': -1, 'counter': 0}
            
        sql = "SELECT * FROM thesis.device where Margin > 0;"
        cursor_local = connection_remote.cursor()
        cursor_local.execute(sql)
        for row in cursor_local:
            margin_devices[row['keyDevice']]={'Margin':row['Margin']}

    thread = threading.Thread(target=initialize_web_server)
    thread.start()


@app.route('/receivedata/', methods=['POST'])
def result():
    if 'starting_code' in request.json:
        print("Booting")
        return "KeepGoing"
    if 'DevEUI_uplink' in request.json:
        #sensorData = SensorDataObject(request.json)
        transformed_string = transform_data(request.json)
        if transformed_string == None:
            return "Keep Going!"
        process_Reading_data(transformed_string)
        process_Incomplete_data(transformed_string)
    else: 
        print(request.json,flush = True)
    return "Keep Going!"
#


@app.route('/commands/', methods=['POST'])
def result_commands():
    ret = resolve_commands(request.json)
    return ret


def resolve_commands(request):
    """ Resolves commands send through POST requests to show information that the server uses"""

    global incomplete_objects_data
    global corrective_measure
    global corrector
    global last_entry_dict
    global margin_devices
    
    command = request['comm']
    if command == 'inc_data':
        string = ''
        for obj in incomplete_objects_data:
            string = string + "ID: " + str(obj.get_Id()) + "\n"
            for field in obj.get_fields():
                string = string + "Field: " + field['id_field'] + " | OP: " + field['op_field'] + " | Value: " + str(
                    field['value_field']) + "\n"
        return string
    elif command == 'data_reset':
        for obj in incomplete_objects_data:
            obj.reset_values(-1)
        return 'Values Resetted to -1'
    elif command == 'temp':
        global temp
        return 'Temperature: ' + str(temp) + 'ºC'
    elif command == 'time_since':#
        global time_latest_entry
        time = datetime.datetime.now() - time_latest_entry
        return 'Time  since last access: ' + time.strftime('H:%M:%S')
    elif command == "correctionStop":
        corrective_measure = False
        return 'Corrective Measures turned off'
    elif command == "correctionStart":
        corrective_measure = True
        return 'Corrective Measures turned on'
    elif command == "showSecsCorrective":
        string = ''
        for entry in corrector.entries:
            string = string + "Device: " + entry.id_d + " | Ideal_Seconds: " + str(entry.ideal_seconds) + "  | DevEUI: "+str(entry.devEui)+"\n"
        string = string + "Status: "+str(corrective_measure)+"\n"
        return string
    elif command == "modIdealSecs":
        id_device = request['id_d']
        value = request['value']
        print(id_device)
        print(value)#
        for entry in corrector.entries:
            if entry.id_d == id_device:
                corrector.set_seconds_one_device(entry.id_d, value)
        string = ''
        for entry in corrector.entries:
            string = string + "Device: " + entry.id_d + " | Ideal_Seconds: " + str(entry.ideal_seconds) + "\n"
        return string
    elif command == "lastPack":
        string = ''
        for entry in last_entry_dict:
            string = string + "Device: "+entry+ " | Counter: " + str(last_entry_dict[entry]['counter']) +" | Seq: "+ str(last_entry_dict[entry]['sequence']) + " | kW: "+ str(last_entry_dict[entry]['kW'])+"\n"
        return string
    elif command == "marginDev":
        string = ''
        for entry in margin_devices:
            string = string + "Device: "+entry+ " | Margin: " + str(margin_devices[entry]['Margin']) +"\n"
        return string
    elif command == "devices":
        global devices
        string = ''
        for entry in devices:
            string = string + entry + " : " + devices[entry]['kd']+"\n"
        return string
    
            

def transform_data(data_sensor):
    global devices
    global last_entry_dict
    global margin_devices 

    data = data_sensor['DevEUI_uplink']
    deveui = data['DevEUI']
    dateTime = None
    id = ''
    kW = -1
    seq = -1
    alert = []
    if deveui not in devices:
        print("Invalid DevEUI",flush=True)
        return None
    if devices[deveui]['dt'] == 'Arduino-TEMP':
        dateTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        id = devices[deveui]['kd']
        temp_value = int(data['payload_hex'][0:4],16)/100+1.3
        transformed_string_temp = {"Time": dateTime,
                                 "id": id,
                                 "temp_value": temp_value}
        reading_temp = ReadingObjectTemperature(transformed_string_temp)
        reading_temp.get_fields_reading()
        reading_temp.sql_open()
        reading_temp.insert_into_sql()
        reading_temp.sql_close()
        return None
        
    if devices[deveui]['dt'] == 'Arduino-PWR':
        dateTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        id = devices[deveui]['kd']
        print(bytearray.fromhex(data['payload_hex']).decode(),flush=True)
        data_after = (bytearray.fromhex(data['payload_hex']).decode()).split(';')
        seq = int(data_after[0])
        if seq == last_entry_dict[id]['sequence']:
            kW = float(data_after[1]) - last_entry_dict[id]['kW']
            alert.append(("Repeated Sequence","Count"))
        else:
            kW = float(data_after[1])
        last_entry_dict[id]['kW'] = float(data_after[1])
        last_entry_dict[id]['sequence'] = int(data_after[0])
        
        if id in margin_devices:
            if kW < margin_devices[id]['Margin']:
                kW = 0
                
    transformed_string = {"Internal": 0,
                          "Time": dateTime,
                          "id": id,
                          "kW": kW,
                          "seq": seq,
                          "alert":alert}
    return transformed_string#


def process_Reading_data(transformed_string):
    """
        Gets the dictionary from the method transform_data(), then proceeds to create a ObjectReading
        that will process the entry into the database.
        Will also log the time of the last entry into the database.

        Parameters
        ----------
        transformed_string : dict
            Dictionary that comes from transform_data()

        """
    print(transformed_string,flush=True)
    global temp
    global time_latest_entry
    global corrector
    
    global margin_devices
    id_var = transformed_string['id']
    if id_var in margin_devices:
            if float(transformed_string['kW']) < margin_devices[id_var]['Margin']:
                transformed_string['kW'] = 0
    
    reading = ReadingObject(transformed_string, temp, 60)
    reading.get_fields_reading()
    reading.sql_open()
    reading.insert_into_sql()
    reading.sql_close()
    if corrective_measure == True:
        corrector.correct(reading.device_input, reading.seconds)
    time_latest_entry = datetime.datetime.now()


def process_Incomplete_data(transformed_string):
    global incomplete_objects_data
    if transformed_string['Internal'] == 0:
        if not timer_running:
            thread_timer = threading.Thread(target=start_Incomplete_Timer)
            thread_timer.start()
        for obj in incomplete_objects_data:
            if obj.check_if_field_exists(transformed_string['id']):
                obj.set_field_value(transformed_string['id'], transformed_string['kW'])
                if obj.check_ready_to_send():
                    return_string = obj.create_send_string(None)
                    process_Reading_data(return_string)
                    obj.reset_values(-1)
                    
def start_Incomplete_Timer():
    global timer_running
    timer_running = True
    timer = DATA_INTERVAL - 1
    time.sleep(timer*60)
    for obj in incomplete_objects_data:
            obj.reset_values(-1)
    gc.collect()
    timer_running = False
    #


def start_runner():
    def start_loop():
        not_started = True
        while not_started:#
            try:
                url = 'https://0.0.0.0:5005/receivedata/'
                payload = {'starting_code': 'starting_code'}
                headers = {'content-type': 'application/json'}
                r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
                if r.status_code == 200:
                    not_started = False
            except:
                pass
            time.sleep(5)#

    thread = threading.Thread(target=start_loop)
    thread.start()


if __name__ == '__main__':
    start_runner()
    app.run(host='0.0.0.0', debug=True, port=5005, ssl_context=('cert.pem', 'key.pem'))  # 10.58.20.35
