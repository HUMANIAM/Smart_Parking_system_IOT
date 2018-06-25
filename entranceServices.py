import RPi.GPIO as GPIO
import time
import UserDB
from flask import Flask, request
import json

app = Flask(__name__)
@app.route('/api/remove/<rfid>/<slot>')
def DeleteClient(rfid, slot):
        done = UserDB.DeleteClient(rfid, slot)
        if done : return "yes"
        else: return "no"

@app.route('/api/IsInside/<rfid>/<slot>')
def isinside(rfid, slot):
        return UserDB.isInside(str(rfid), int(slot))

"""
@app.route('/api/IsInside', methods=['GET', 'POST'])
def isInside():

        rfids = request.get_json(silent=True)
        json.dumps(rfids)
        print(rfids["key"])
        #print(str(rfids)) 
        return json.dumps(rfids)
"""

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

