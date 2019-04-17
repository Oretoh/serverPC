import json
import SensorData
import pymysql.cursors

connection_remote = pymysql.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="test",
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor,
        autocommit = True)

cursor_local = connection_remote.cursor()

data_string = '{"DevEUI_uplink": {"Time": "2018-10-25T17:01:11.313+00:00", "DevEUI": "A8610A3130377313", "FPort": 15, "FCntUp": 0, "ADRbit": 1, "MType": 4, "FCntDn": 1, "payload_hex": "7b2263757272656e74223a3232327d", "mic_hex": "3aefb9ba", "Lrcid": "0000000F", "LrrRSSI": -112.0, "LrrSNR": 2.5, "SpFact": 12, "SubBand": "G1", "Channel": "LC1", "DevLrrCnt": 2, "Lrrid": "10000001", "Late": 0, "LrrLAT": 38.749283, "LrrLON": -9.153593, "Lrrs": {"Lrr": [{"Lrrid": "10000001", "Chain": 0, "LrrRSSI": -112.0, "LrrSNR": 2.5, "LrrESP": -113.937759}, {"Lrrid": "10000002", "Chain": 0, "LrrRSSI": -118.0, "LrrSNR": -12.75, "LrrESP": -130.974655}]}, "CustomerID": "1100000000", "CustomerData": {"alr": {"pro": "LORA/Generic", "ver": "1"}}, "ModelCfg": "0", "InstantPER": 0.0, "MeanPER": 0.0, "DevAddr": "0370E515"}}'
data_json = json.loads(data_string)
data = data_json['DevEUI_uplink']
sensordata = SensorData.SensorDataObject(data['Time'],data['DevEUI'],data['FPort'],data['FCntUp'],data['ADRbit'],data['MType'],data['FCntDn'],
                              data['payload_hex'],bytearray.fromhex(data['payload_hex']).decode(),data['mic_hex'],data['Lrcid'],
                              data['LrrRSSI'],data['LrrSNR'],data['SpFact'],data['SubBand'],data['Channel'],data['DevLrrCnt'],data['Lrrid'],
                              data['Late'],data['LrrLAT'],data['LrrLON'], data['CustomerID'],data['CustomerData']['alr']['pro']+" v"+data['CustomerData']['alr']['ver'],
                              data['ModelCfg'],data['InstantPER'],data['MeanPER'],data['DevAddr'])
cursor_local.execute(sensordata.generateString(), sensordata.generateValues())