import pymysql

class DeviceObject:
    keyDevice = ''
    type = ''
    name = ''
    room = ''
    building = ''

    def __init__(self,keyDevice):
        self.keyDevice = keyDevice

    def getDeviceKey(self):
        return self.keyDevice

    def setAttributes(self, type, name, room, building):
        self.type = type
        self.name = name
        self.room = room
        self.building = building

    def generate_insert_string(self):
        sql = 'INSERT INTO thesis.device (keyDevice, type, name, room, building) VALUES (%s,%s,%s,%s,%s);'
        return sql

    def get_device(self, keyDevice):
        sql = "SELECT * FROM thesis.device where keyDevice = %s;"
        cursor_local = self.connection_remote.cursor()
        cursor_local.execute(sql, keyDevice)
        for row in cursor_local:
            return row

    def generate_tuple(self):
        return (self.keyDevice, self.type, self.name, self.room, self.building)

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
        cursor_local.execute(self.generate_insert_string(), self.generate_tuple())

    def SQLClose(self):
        self.connection_remote.close()

if __name__ == '__main__':
    print("Insert Device")
    keyDevice = input("KeyDevice: ")
    type = input("Type of Device: ")
    name = input("Name: ")
    room = input("Room: ")
    building = input("Building: ")

    obj = DeviceObject(keyDevice)
    obj.setAttributes(type, name, room, building)
    obj.SQLOpen()
    obj.insertIntoSQL()
    obj.SQLClose()