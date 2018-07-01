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
activeThreads = [0, 0]
PB_SLOTS = [18, 31]

#intialize slots leds with False
for i in range(SLOT_COUNT):
	GPIO.setup(TRIGS[i],GPIO.OUT)
	GPIO.setup(ECHOS[i],GPIO.IN)
	GPIO.setup(SLOTS[i], GPIO.OUT)
	GPIO.output(SLOTS[i], False)
	GPIO.setup(PB_SLOTS[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
			UserDB.changestate(self.slot, 1)

######################################

			
class leavethread (threading.Thread):
	def __init__(self, slot):
		threading.Thread.__init__(self)
		self.slot = slot
		
	def run(self):
		try:
			#wait till the client push the push button if he/she doesn't push it through 5 min ignore the request
			print(' leave  thread')
			t = time.time()
			dt=0
			state= True
			
			#wait the client press the pB if he don't through 5 min ignore his request
			while (dt < 300 and state == True) :
					dt = time.time() - t
					state = GPIO.input(PB_SLOTS[self.slot - 1])
					
			#open the slot
			if state == False:
				while GPIO.input(PB_SLOTS[self.slot - 1]) == False:
					time.sleep(0.2)

				print('client push the button')
				GPIO.output(SLOTS[self.slot - 1], True)

				#wait 10 min untill the user take his/her car
				t = time.time()
				dt=0
				dd= distance(self.slot - 1)
				print(dd)

				while ((dt < 600 and dd < 200) or (dd > 11 and dd < 200)):
					dt = time.time() - t
					dd = distance(self.slot - 1)
					print(dd)
				
				#close the slot lock
				GPIO.output(SLOTS[self.slot - 1], False)
				
			if dd>200:
				#make slot empty
				UserDB.changestate(self.slot, 0)
				
		except Exception as e:
			print('error in leavethread : ', e)
			
		finally:
			activeThreads[self.slot - 1] = 0
					
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
		
	
@app.route('/api/openslot', methods=['GET', 'POST'])
def leavecar():
	try:
		
		jsData = request.get_json(silent=True)
		if type(jsData) == 'str':
			jsData = json.loads(jsData)

		print("open slot", jsData['slot'])
			
		if activeThreads[jsData['slot'] - 1] == 0:
			print("slot : ", jsData["slot"])
			thread1 = leavethread(jsData["slot"])
			thread1.start()
			activeThreads[jsData['slot'] - 1] = 1
		return '1'
	except Exception as e:
		print(e)
		return '0'

if __name__ == '__main__':
	time.sleep(1)
	app.run(debug=True, host='0.0.0.0')
	print("Wainting for requests")


