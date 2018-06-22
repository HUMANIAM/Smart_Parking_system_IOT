import RPi.GPIO as GPIO
import time

Buzzer = 3

def setup():
	global Buzzer
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(Buzzer, GPIO.OUT)
	GPIO.output(Buzzer, GPIO.LOW)

def on():
	GPIO.output(Buzzer, GPIO.HIGH)

def off():
	GPIO.output(Buzzer, GPIO.LOW)

def beep(x):
	on()
	time.sleep(x)
	off()


	
