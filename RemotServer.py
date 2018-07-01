import urllib.request as urlrequest
#import requests
import json
import sys
import time
from socket import timeout
import eventlet
GARAGE_ID = '1'
url = 'http://156.217.116.191:8000/api/getNewReservations/'
  
def GetNews():
    users = []
    user = []
    try:

        #get new reservation from the server
        garage = (json.dumps({"ID":1})).encode('utf-8')
        req = urlrequest.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', len(garage))
        newUsers = urlrequest.urlopen(req, garage, timeout=10).read().decode()
            
        #newUsers = urlrequest.urlopen(url, timeout=10).read().decode()
        
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


