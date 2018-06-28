import urllib.request as urlrequest
import json
import sys
import time
ulr = 'http://192.168.1.14:8000/api/rfid'
    
def GetNews():
    users = []
    user = []
    try:
        newUsers = urlrequest.urlopen(ulr).read().decode()
        newUsers = json.loads(newUsers)
		
        for usr in newUsers:
            if isPermitted(usr[2], usr[3]):
                #get user data
                user.append(usr[1])         #RFID
                user.append(usr[0])         #first name
                user.append(usr[2])         #reservation time
                user.append(usr[3])         #maximum hours
                
                #append this user to users
                users.append( user)
                user=[]
        
    except Exception as e:
        print('error during get new users', e)

    users.append(["3814137172", "abdo", "2018-04-25 07:06:13", 0.4])

    return users


