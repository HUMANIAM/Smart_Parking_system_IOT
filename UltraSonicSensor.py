import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
import time

TRIG = 11
ECHO = 13

GPIO.setup(TRIG,GPIO.OUT)  

GPIO.setup(ECHO,GPIO.IN)

def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)

    GPIO.output(TRIG, False)

    pulse_start = pulse_end = time.time()

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start

    distance = (pulse_duration * 34300)/2

    distance = round(distance, 2)

    time.sleep(1.5)
    
    return distance



def IsPassed():    
    print('wait untill the car passing the gate')
    d = distance()
    #print("before passing ")
    while(d> 12):
        d = distance()
        print(d)
        pass

    #print('during passing')
    while(d<= 12):
        d = distance()
        print(d)
        pass
   
    print('the gate is closed')
    return True

