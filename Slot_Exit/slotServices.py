"""
this simple server do very simple tasks
1- listen to car entrance RPI. if there is a new car want to enter the a slot
2- listen to server if a client want to cancel his reservation and want to leave the garage
"""

import RPi.GPIO as GPIO
import time
import UserDB
import threading
from flask import Flask, request

#######################################
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)				

SLOT_COUNT = 2
SLOTS = [32, 33]			#slots bins			
ECHOS = [10, 37]			#echos bins of ultrasonic
TRIGS = [8, 35]			#triggers bins of ultrasonic

#intialize slots leds with False
for i in range(SLOT_COUNT):
	GPIO.setup(TRIGS[i],GPIO.OUT)
	GPIO.setup(ECHOS[i],GPIO.IN)
	GPIO.setup(SLOTS[i], GPIO.OUT)
	GPIO.output(SLOTS[i], False)


######################################

# calculate the distance		
def distance(slot):
	GPIO.output(TRIGS[slot], True)
	time.sleep(0.00001)
	
	GPIO.output(TRIGS[slot], False)
	pulse_start = pulse_end = time.time()
	
	while GPIO.input(ECHOS[slot])==0:
		pulse_start = time.time()
		
	while GPIO.input(ECHOS[slot])==1:
		pulse_end = time.time()
		
	pulse_duration = pulse_end - pulse_start
	distance = (pulse_duration * 34300)/2
	distance = round(distance, 2)
	
	time.sleep(1.5)
	return distance
	
######################################
			
class Openthread (threading.Thread):
	def __init__(self, rfid, slot):
		threading.Thread.__init__(self)
		self.slot = slot
		self.rfid = rfid
		
	def run(self):
		#open the slot
		GPIO.output(SLOTS[self.slot - 1], True)
		UserDB.fillSlot(self.rfid, self.slot)
		#time.sleep(30)

		#wait the car till enter the slot. if not come after 6 min close the slot
		t = time.time()
		dt=0
		dd= distance(self.slot - 1)
		
		#wait if time is less than 6 min and dd greater than 11
		#wait if dd between 12 cm and 2.5 meter
		while ((dt < 600 and dd > 11) or (dd > 11 and dd < 250)):
				dt = time.time() - t
				dd = distance(self.slot - 1)
				print(dd)
				
		#close the slot
		print('the slot is closed')
		time.sleep(1)
		GPIO.output(SLOTS[self.slot - 1],False)
		
		#change state of the slot from empty to busy 
		if dd < 11 :
			UserDB.changestate(self.slot)

######################################		

app = Flask(__name__)
@app.route('/api/newcar', methods=['GET', 'POST'])
def newCar():
	try:
		jsData = request.get_json(silent=True)
		if type(jsData) == 'str':
			jsData = json.loads(jsData)
			
		thread1 = Openthread(jsData["RFID"], jsData["slot"])
		thread1.start()
		return '1'
	except:
		return '0'
		
	
@app.route('/api/openslot', methods=['GET', 'POST']))
def leavecar():
	try:
		jsData = request.get_json(silent=True)
		if type(jsData) == 'str':
			jsData = json.loads(jsData)
			
		thread1 = Openthread(jsData["RFID"], jsData["slot"])
		thread1.start()
		return '1'
	except:
		return '0'

if __name__ == '__main__':
	time.sleep(1)
	app.run(debug=True, host='0.0.0.0')
	print("Wainting for requests")


