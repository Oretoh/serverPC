# import http.client as httplib
# import time
# import datetime
#
# if __name__ == '__main__':
#     httplib.debuglevel = 0
#     content_type_header = "application/json"
#
#     data = {    'room':         "Living Room",
#                 'temp':         23.45,
#                 'humidity':     50.00,
#                 'timestamp':    str(datetime.datetime.now())
#            }
#
#     headers = {'Content-Type': content_type_header}
#     print("Posting %s" % data)
#
#     while True:
#         conn = httplib.HTTPSConnection('127.0.0.1', 5005)
#         print(conn)
#         conn.request('POST', '/testingdata/', data, headers)
#         time.sleep(3)

# import http.client, urllib.parse
# params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
# headers = {"Content-type": "application/x-www-form-urlencoded",
#            "Accept": "text/plain"}
# conn = http.client.HTTPSConnection("127.0.0.1",5005)
# conn.request("POST", "/testingdata/", params, headers)
# response = conn.getresponse()
# print(response.status, response.reason)
#
# data = response.read()
# print(data)
#
# conn.close()

import requests
import json

# {"id":"avac_aud1","kW":5, "current":3}
# {"id":"avac_aud2","kW":3, "current":1.5}
# {"id":"light_aud1","kW":2, "current":1.3}
# {"id":"light_aud2","kW":3, "current":1.4}
# {"id":"total_light_other_aud1_aud2","kW":10, "current":9}

url = 'https://192.168.1.88:5005/receivedata/'
payload = {'DevEUI_uplink': {'Time': '2018-10-25T17:01:11.313+00:00', 'payload_hex': '7b226964223a22617661635f61756431222c226b57223a352c202263757272656e74223a337d'}}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
payload = {'DevEUI_uplink': {'Time': '2018-10-25T17:01:11.313+00:00', 'payload_hex': '7b226964223a22617661635f61756432222c226b57223a332c202263757272656e74223a312e357d'}}
r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
payload = {'DevEUI_uplink': {'Time': '2018-10-25T17:01:11.313+00:00', 'payload_hex': '7b226964223a226c696768745f61756431222c226b57223a322c202263757272656e74223a312e337d'}}
r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
payload = {'DevEUI_uplink': {'Time': '2018-10-25T17:01:11.313+00:00', 'payload_hex': '7b226964223a226c696768745f61756432222c226b57223a332c202263757272656e74223a312e347d'}}
r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
payload = {'DevEUI_uplink': {'Time': '2018-10-25T17:01:11.313+00:00', 'payload_hex': '7b226964223a22746f74616c5f6c696768745f6f746865725f617564315f61756432222c226b57223a31302c202263757272656e74223a397d'}}
r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
payload = {'DevEUI_uplink': {'Time': '2018-10-25T17:01:11.313+00:00', 'payload_hex': '7b226964223a226c696768745f61756432222c226b57223a332c202263757272656e74223a312e347d'}}
r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)







# import pyowm
# owm = pyowm.OWM('daa8ea25a8ef817b9e2a10d4569fa27f')
# observation_list = owm.weather_at_coords(38.74868698676801,-9.155080982973573)
# temp = observation_list.get_weather().get_temperature('celsius')['temp']
# print(temp)