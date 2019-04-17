import json
import pymysql
from Correction.CorrectionObject import CorrectionObject
from Correction.DownlinkMsg import LPLCS
from random import randint


class CorrectionAlgorithm:
    id_a = ''
    entries = []

    def __init__(self, id_a):
        self.id_a = id_a
        self.add_devices()
        #

    def add_devices(self):
        self.connection_remote = pymysql.connect(
            host="127.0.0.1",
            user="admin",
            passwd="lisonco20",
            database="thesis",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True)
        
        sql = "SELECT * FROM thesis.device where active = 1 and Correction > 1;"
        cursor_local = self.connection_remote.cursor()
        cursor_local.execute(sql)
        for row in cursor_local:
            self.entries.append(CorrectionObject(row['keyDevice'], row['devEui']))
        for r in self.entries:
            print(r,flush=True)
        
        #with open('devices.json') as f:
            #data = json.load(f)
           # for objects in data:
           #     self.entries.append(CorrectionObject(objects['id'], objects['devEUI']))
        #f.close()
        #

    def set_seconds_one_device(self, id_d, ideal_sec):
        for entry in self.entries:
            if entry.id_d == id_d:
               entry.ideal_seconds = ideal_sec

    def correct(self, id_d, seconds):
        seconds = int(seconds)
        var = randint(1, 3)
        print(var,flush=True)
        if var == 3:
            for entry in self.entries:
                if entry.id_d == id_d:
                    lplcs = LPLCS()
                    lplcs.setDevEui(entry.devEui)
                    if seconds == int(entry.ideal_seconds):
                        return
                    if seconds > int(entry.ideal_seconds):
                        lplcs.sendTPMsgToClient(str(1))#+
                        return
                    if seconds < int(entry.ideal_seconds):
                        lplcs.sendTPMsgToClient(str(-1)) #-
                        return