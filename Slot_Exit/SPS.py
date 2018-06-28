import RPi.GPIO as GPIO
import MFRC522
import ServoMotor
import UltraSonicSensor
import signal
import sys
import time 
import UserDB
import buzzer


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
    ServoMotor.GPIO.cleanup()
    UltraSonicSensor.GPIO.cleanup()
    buzzer.GPIO.cleanup()

def setupComponents():
    #initialize buzzer
    buzzer.setup()

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
            
            #alter the user that the card is read
            buzzer.beep(1)

            ok = UserDB.allowExit(Uid)

            if ok :
                ServoMotor.OpenGate()   #open the gate
                
                #wait till the car pass the gate
                if(UltraSonicSensor.IsPassed()):
					time.sleep(2)
					ServoMotor.CloseGate()  #close the gate
					
					#remove this user from the db of slots
					#and also from the db of car entrance
					UserDB.freeSlot(Uid) 

            else:
                print("this tag doesn't have car inside the garage")
                print("enter the correct one")


if __name__ == "__main__":
    main()
                    
        


