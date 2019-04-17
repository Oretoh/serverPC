
import json
import parser
import datetime
from binascii import hexlify

class ReadingIncomplete:
    id = ''
    fields = []

    def __init__(self, object):
        self.id = object['id']
        self.fields = object['fields']

    def get_Id(self):
        return self.id

    def get_fields(self):
        return self.fields

    def check_if_field_exists(self, f_name):
        exists = False
        for field in self.fields:
            if field['id_field'] == f_name:
                exists = True
        return exists

    def reset_values(self, value):
        for field in self.fields:
            field['value_field'] = value

    def check_ready_to_send(self):
        ready = True
        for field in self.fields:
            if field['value_field'] <= -1:
                ready = False
        return ready

    def set_field_value(self, f_name, value):
        for field in self.fields:
            if field['id_field'] == f_name:
                field['value_field'] = value

    def create_send_string(self, time):
        string_calc = ''
        alert=[]
        for field in self.fields:
            string_calc = string_calc + field['op_field'] + str(field['value_field'])
        value = eval(parser.expr(string_calc).compile())
        if time == None:
            time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
        string_to_send = {"Internal": 1,
                          "Time": time,
                          "id": self.id,
                          "kW": value,
                          "alert":alert}
        return string_to_send



list_incompletes = []





