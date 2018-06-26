import RPi.GPIO as GPIO
import time
import UserDB
import ast
from flask import Flask, request
import json

app = Flask(__name__)
"""
@app.route('/api/remove/<rfid>/<slot>')
def DeleteClient(rfid, slot):
        done = UserDB.DeleteClient(rfid, slot)
        if done : return "yes"
        else: return "no"


@app.route('/api/IsInside/<rfid>/<slot>')
def isinside(rfid, slot):
        return UserDB.isInside(str(rfid), int(slot))

"""
#remove a client from the local DB
@app.route('/api/remove', methods=['GET', 'POST'])
def DeleteClient():
        jsData = request.get_json(silent=True)
        if type(jsData) == 'str':
                jsData = json.loads(jsData)
        done = UserDB.DeleteClient(jsData["RFID"], jsData["slot"])
        if done : return "yes"
        else: return "no"

#check if clients in local DB or no
@app.route('/api/IsInside', methods=['GET', 'POST'])
def isInside():
        jsData = request.get_json(silent=True)

        if type(jsData) == 'str':
                jsData = json.loads(jsData)
       
        i = len(jsData["RFID"])
        j = 0
        response = {"status":[]}

        while j < i:
                response["status"].append(UserDB.isInside(str(jsData["RFID"][j]), int(jsData["slot"][j])))
                j = j + 1

        print(response)
        response = json.dumps(response).encode('utf-8')
        
        
        return "response"
        


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

