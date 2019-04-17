import json

import requests


def start():
    url = 'https://192.168.1.80:5005/commands/'
    headers = {'content-type': 'application/json'}

    while True:
        var = input('Command: ')
        if var == '.inc_data':
            payload = {'comm': 'inc_data'}
            r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
            print(r.text)
        elif var == '.reset_inc':
            payload = {'comm': 'data_reset'}
            r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
            print(r.text)
        elif var == '.temp':
            payload = {'comm': 'temp'}
            r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
            print(r.text)
        elif var == '.time_since':
            payload = {'comm': 'time_since'}
            r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
            print(r.text)
        elif var == '.help':
            print('.inc_data | view incomplete data in memory')
            print('.reset_inc | reset incomplete data in memory')
            print('.temp | get external temperature saved in memory')
            print('.time_since | get time since latest entry in MySQL')


if __name__ == '__main__':
    start()
