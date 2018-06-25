import RPi.GPIO as GPIO
import ServoMotor
import UltraSonicSensor
import signal
from module.MFRC522 import MFRC522
from module.pinos import PinoControle
import TwoRfid
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
#MIFAREReader = MFRC522.MFRC522()

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
    global nfc

    # Scan for cards    
    #(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    gid1,gid2 = nfc.obtem_nfc_rfid()

    # If a card is found
    #if status == MIFAREReader.MI_OK:
        #print ("Card detected")

    # Get the UID of the card
    #(status,uid) = MIFAREReader.MFRC522_Anticoll()
    
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
    nfc = TwoRfid.Nfc522()          #create object to read from 2 different rfid
    while continue_reading:

        #read RFID
        #found, Uid = readRFID()
        gid1,gid2 = nfc.obtem_nfc_rfid()

        #handle car gate
        if not gid1==0:
            print("rfid reader of car gate read: ", gid1 )
            buzzer.beep(1)

            name, slot, state = UserDB.AllowAccess(str(gid1), 0)
            if(state == 0):                                 #this person has a reservation
                lcd.message("WELCOME ", name)

                time.sleep(2)
                lcd.message("Go To Slot", str(slot))
                ServoMotor.OpenGate()   #open the gate
                
                 #wait till the car pass the gate
                if(UltraSonicSensor.IsPassed()):

                    #make microController open specific slot

                    UserDB.changeState(gid1)
                    time.sleep(3)
                    ServoMotor.CloseGate()  #close the gate

            elif(state == -2):                              #this person not has a reservation
                lcd.message("Please ", "Reserve First")

            time.sleep(5)
            lcd.message("WELCOME IN", "SMART PARKING" )


        #handle person gate
        if not gid2==0:
            print("rfid reader of person gate read: ", gid2 )
            buzzer.beep(1)

            name, slot, state = UserDB.IsReserve(str(gid2), 1)
            if state == 1:                                      #this person has a car inside the garage
                #open the gate
                lcd.message("Here you are", "The Gate is open")
                GPIO.output(PERSON_GATE, True)
                time.sleep(6)
                GPIO.output(PERSON_GATE, False)

                #open cancellation slots
                #slots = RemotServer.cancellation(rfid, GARAGE_ID)
                """
                if len(slots) != 0:
                    lcd.message("your car is", "ready to leave")
                    for s in slots:
                        #open the slot
                        i=5
                """ 
            else :
                lcd.message("Sorry You don't ", "Have car inside" )

            time.sleep(5)
            lcd.message("WELCOME IN", "SMART PARKING" )



if __name__ == "__main__":
    main()
                    
        


