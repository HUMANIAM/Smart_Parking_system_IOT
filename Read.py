import RPi.GPIO as GPIO
import MFRC522
import buzzer
import ServoMotor
import UltraSonicSensor
import signal
import time 
import MySQLdb

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    
# Setup buzzer
buzzer.setup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
prelucky = ""
timedetection = 0
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        
        lucky = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
        if lucky != prelucky :
            timedetection = time.time()
            prelucky = lucky
            
            connect = MySQLdb.connect(host="localhost" , port = 3306 , user = "root" , passwd = "Abdo" , db = 'SmartGarrage' , charset='utf8')
            cursor = connect.cursor()
            sql = """ insert into Sensors (SensorType,Sensor_Reading) values ('RFID',%s)"""
            
            cursor.execute(sql,lucky)           #execute the command
            connect.commit()
            connect.close()
            
            buzzer.beep(1)          #alter client that RFID is read
            ServoMotor.OpenGate()   #open the gate

            #wait till the car pass the gate
            if(UltraSonicSensor.IsPassed()):
                time.sleep(5)
                ServoMotor.CloseGate()  #close the gate
            
        if(time.time() - timedetection > 10): prelucky = ""   

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"
    
