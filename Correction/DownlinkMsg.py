#!/usr/bin/env python3

import sys
import http.client, urllib.parse
import json
import binascii

import ssl
import http.server
import socketserver




class LPLCS:

    TPHTTPSConnectionHost    = "iscte.actility.local"

    TPReqTokenURL            = "/thingpark/dx/admin/latest/api/oauth/token"
    TPClient_id              = "tpe-api/Joao.Carlos.Ferreira@iscte-iul.pt"
    TPClient_secret          = "iscte#2018"
    FSTokenPath              = "./TPToken.dat"

    TPReqDownlinkMessagesURL = ""
    TPSecurityParamsAsId     = "TWA_1100000000.20.AS"
    TPSecurityParamsAsKey    = "2735f9025ff17e29476ad6c8f85014d2"





    def getTPToken(self, iForce = False):
        vToken = ""
        if (not iForce):
            try:
                with open(self.FSTokenPath, 'r') as f:
                    vToken = f.read()
            except:
                pass

        if (vToken == ""):
            headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
            params = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": self.TPClient_id, "client_secret": self.TPClient_secret})
            #params = json.dumps({"grant_type": "client_credentials", "client_id": defs.TPClient_id, "client_secret": "iscte#2018"})
            conn = http.client.HTTPSConnection(self.TPHTTPSConnectionHost, context = ssl._create_unverified_context())
            try:
                conn.request("POST", self.TPReqTokenURL, params, headers)
                response = conn.getresponse()
                data = response.read().decode()
            finally:
                conn.close()
            print(response.status, response.reason)
            print(data)
            vToken = json.loads(data)["access_token"]
            try:
                with open(self.FSTokenPath, 'w') as f:
                    f.write(vToken)
            except:
                pass
        return vToken

    def sendTPMsgToClient(self, iMsgToClient):
        payload = str(binascii.b2a_hex(iMsgToClient.encode("utf-8")), "utf-8")
        for vForce in (False, True):
            headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": "Bearer " + self.getTPToken(vForce) }
            params = json.dumps({"payloadHex" : payload, "targetPorts" : "1", "securityParams": {"asId": self.TPSecurityParamsAsId, "asKey": self.TPSecurityParamsAsKey}})
            conn = http.client.HTTPSConnection(self.TPHTTPSConnectionHost, context = ssl._create_unverified_context())
            try:
                conn.request("POST", self.TPReqDownlinkMessagesURL, params, headers)
                response = conn.getresponse()
                data = response.read().decode()
            finally:
                conn.close()
            print(response.status, response.reason)
            print(data)
            if ("message" not in json.loads(data)):
                break

    def setDevEui(self, devEUI):
        self.TPReqDownlinkMessagesURL = "/thingpark/dx/core/latest/api/devices/"+devEUI+"/downlinkMessages"


def main():
    lplcs = LPLCS()
    lplcs.setDevEui('a8610a31303f6513')
    lplcs.sendTPMsgToClient('1')

if (__name__ == "__main__"):
    main()
