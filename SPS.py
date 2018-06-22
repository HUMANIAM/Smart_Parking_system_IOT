import RPi.GPIO as GPIO
import MFRC522
import ServoMotor
import UltraSonicSensor
import signal
import sys
import time 
import UserDB
import lcd
import buzzer
import RemotServer

continue_reading = True
PERSON_GATE = 36
GARAGE_ID   = 1

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    lcd.GPIO.cleanup()
    ServoMotor.GPIO.cleanup()
    UltraSonicSensor.GPIO.cleanup()
    buzzer.GPIO.cleanup()

def setupComponents():
    #initialize buzzer
    buzzer.setup()
    
    #intialize lcd
    lcd.lcd_init()
    time.sleep(1)
    lcd.message("WELCOME ", "SMART PARKING")

    #set person gate pin as output pin
    GPIO.setup(PERSON_GATE, GPIO.OUT)
    GPIO.output(PERSON_GATE, False)

    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)



    # Welcome message
    print ("Welcome to the MFRC522 data read example")
    print ("Press Ctrl-C to stop.")


def readRFID():
    global MIFAREReader

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    
    #if status is okey
    if status == MIFAREReader.MI_OK:
        Uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
        return True, Uid
    else:
        return False, ""

def main():
    #intialize the components of the project
    setupComponents()
    
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate

    while continue_reading:
        #read RFID
        found, Uid = readRFID()
        
        if found:
            person = False
            # Print UID
            print ("Card read UID: "+Uid)

            name, slot, state = UserDB.AllowAccess(Uid)

            #alter the user that the card is read
            buzzer.beep(1)
             
            if(state == 1):
                lcd.message("WELCOME ", name)

                time.sleep(2)
                lcd.message("Go To Slot", str(slot))
                ServoMotor.OpenGate()   #open the gate
                
                 #wait till the car pass the gate
                if(UltraSonicSensor.IsPassed()):

                    #make microController open specific slot

                    UserDB.changeState(Uid)
                    time.sleep(3)
                    ServoMotor.CloseGate()  #close the gate

            elif(state == -2):
                lcd.message("Please ", "Reserve First")

            else:
 
				#check if the client enter the garage to get something from a car
				#or for get out a car from the garage. we can do that by ask the server

                person = True
                #open the gate
                lcd.message("Here you are", "The Gate is open")
                time.sleep(3)
                
                #light a led refers to that the gate is opened
                GPIO.output(PERSON_GATE, True)
                
                slots = RemotServer.cancellation(rfid, GARAGE_ID)		#which slot he/she will leave?
                
                if len(slots) != 0:
                	lcd.message("your car is", "ready to leave")
                	for s in slots:
                		#open the slot
                		i=5

            if(not person): time.sleep(6)
            lcd.message("WELCOME IN", "SMART PARKING" )


if __name__ == "__main__":
    main()
                    
        


