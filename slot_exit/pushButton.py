import RPi.GPIO as GPIO
import time

button1 = 18

button2 = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
	 try:
	 	while True:
	 		button_state1 = GPIO.input(button1)
	 		button_state2 = GPIO.input(button2)
	 		if  button_state2 == False :
	 			print('Button1 Pressed...')
	 			while GPIO.input(button2) == False:
	 				time.sleep(0.2)
	 				
	 				 				
	 		if  button_state1 == False :
	 			print('Button2 Pressed...')
	 			while GPIO.input(button1) == False:
	 				time.sleep(0.2)

	 except KeyboardInterrupt:
	 	print 'keyboard interrupt detected'
	 	GPIO.cleanup()
