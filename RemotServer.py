import urllib.request as urlrequest
import json
import sys
import time
from socket import timeout
import eventlet

GARAGE_ID = '1'
ulr = 'http://156.217.227.244:8000/api/getNewReservations/' + GARAGE_ID 
  
def GetNews():
    users = []
    user = []
    try:
        newUsers = urlrequest.urlopen(ulr, timeout=10).read().decode()
        
        newUsers = json.loads(newUsers)
		
        for usr in newUsers:
            #get user data
            user.append(usr["RFID"])         	#RFID
            user.append(usr["name"])        	 #first name
            user.append(usr["slot"])			#slot
            
            #append this user to users
            users.append( user)
            user=[]
        print(users)
        
    except Exception as e:
        print('error during get new users', e)

    #users.append(["3814137172", "abdo", "2018-04-25 07:06:13", 0.4])

    return users


