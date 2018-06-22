import RPi.GPIO as GPIO
import time
import buzzer
import lcd
import threading
from flask import Flask, request
"""
this simple server do very simple tasks
1- remove car that leaves the garage from the DB of RPI
2- listen if there is a client want to open a slot while he/she in the garage

"""
GPIO.setmode(GPIO.BOARD)
j=0
PERSON_GATE = 36
GPIO.setup(PERSON_GATE, GPIO.OUT)
GPIO.output(PERSON_GATE, False)


class sthread (threading.Thread):
	def __init__(self, slot):
		threading.Thread.__init__(self)
		self.slot = slot
		
	def run(self):
		if self.slot == "1":
			while True :
				buzzer.beep(5)
				time.sleep(2)
		else:
			while True:
				GPIO.output(PERSON_GATE, True)
				time.sleep(3)
				GPIO.output(PERSON_GATE,False)
				time.sleep(3)
			

app = Flask(__name__)
@app.route('/leave')
def leave():
	slot = request.args.get('slot')
	print("slot type", type(slot))

	thread1 = sthread(slot)
	thread1.start()
	"""
		thread1 = buzzerClass(1)
		thread1.start()
		j = j + 1
		print("start buzzer")
	"""
	return slot
	
@app.route('/open')
def open():
	#
	slot = request.args.get('slot')
	i=0
	"""
	while True :
		if i%2 == 0:
			lcd.message("even", "number")
		else:
			lcd.message("odd", "number")
			
		time.sleep(7)
		i = i + 1
		"""
	return slot

if __name__ == '__main__':
	buzzer.setup()
	lcd.lcd_init()
	time.sleep(1)
	lcd.message("WELCOME ", "SMART PARKING")
	app.run(debug=True, host='0.0.0.0')


