import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)  #set schema numbering
GPIO.setwarnings(False)
servo_pin = 40

GPIO.setup(servo_pin,GPIO.OUT)  #set pin 32 as out pin
pwm=GPIO.PWM(servo_pin, 50)     #create obj of PWM with 50HZ


pwm.start(6)   # start at full left position
time.sleep(0.2)
pwm.stop()
del pwm
           

def OpenGate():
    pwm=GPIO.PWM(servo_pin, 50)     #create obj of PWM with 50HZ
    pwm.start(2)
    time.sleep(0.4)
    pwm.stop()
    del pwm
    pass

def CloseGate():
    pwm=GPIO.PWM(servo_pin, 50)     #create obj of PWM with 50HZ
    pwm.start(6)
    time.sleep(0.4)
    pwm.stop()
    del pwm
    pass




   
