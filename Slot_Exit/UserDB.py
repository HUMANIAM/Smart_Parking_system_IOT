import sqlite3 as sqlite
import time
import requests
import json

db ='slots.db'
conn = sqlite.connect(db)
cursor = conn.cursor()

#name, slot, rfid 
GARAGE_ID = '1'
urls = 'http://156.217.227.244:8000/api/leaveSlot/' + GARAGE_ID
urlg = 'http://192.168.1.10:5000/api/remove'        
                
try:
	cursor.execute('''CREATE TABLE IF NOT EXISTS Slot(
	slot INTEGER primary key not null,
	RFID TEXT default null,
	state INTEGER default 0
	)''')
	
	for i in range(1, 10):
		cursor.execute('''INSERT OR IGNORE INTO Slot (slot) VALUES(?)''', (i,))
		
	conn.commit()
	conn.close()
except Exception as e:
        print(e)
	

def DBConnect():
    global conn
    global cursor
    try:
        conn = sqlite.connect(db)
        cursor = conn.cursor()
        return True
    except Exception as e:
        print(e)
        return False

def CloseDB():
    conn.close()
    return

def changestate(slot):
	try:
		while(DBConnect() != True):
			time.sleep(2)
			
		cursor.execute("UPDATE Slot SET state = ? WHERE slot = ?", (1, slot))
		conn.commit()
	
	except Exception as e :
		print('error during update : ', e)
	
	finally:
		CloseDB()
		
		
def fillSlot(rfid, slot):
	try:
		while(DBConnect() != True):
			time.sleep(2)
			
		cursor.execute("UPDATE Slot SET RFID = ? WHERE slot = ?", (rfid, slot))
		conn.commit()
	
	except Exception as e :
		print('error during update : ', e)
	finally:
		CloseDB()
	
def freeSlot(rfid):
	try:
		
		while(DBConnect() != True):
			time.sleep(3)
			
		
		cursor.execute("SELECT * FROM Slot WHERE RFID = ? AND state = ?", (rfid, 0))
		slots = cursor.fetchall()
		
		data = {"RFID":[], "slot":[]}
		
		for slot in slots:
			data["RFID"].append(slot[1])
			data["slot"].append(slot[0])
			
			#change slot data (state=0, rfid=null)
			cursor.execute("UPDATE Slot SET RFID = ?, state = ? WHERE slot = ?", (None,  0, slot[0]))
			
		conn.commit()
		print(data)
		
		#remove from the car entrance
		headers = {'content-type':'application/json'}
		okg = requests.post(urlg, data=json.dumps(data), headers=headers, verify=False, timeout=10)
		
		#remove from the server
		#oks = requests.post(urls, json.dumps(data), headers=headers, verify=False, timeout=10)
		
		oks = '0'
		if okg == '0':
			#do something to handle that
			i=0
		if oks == '0':
			#do something to handle failure
			i=0

	except Exception as e :
		  print('error during freeslots: ', e)
		  
		
	finally:
		CloseDB()
			

def allowExit(rfid):
	
	try:
		
		if(DBConnect() != True): return False
		
		cursor.execute("SELECT * FROM Slot WHERE RFID = ? AND state = ?", (rfid, 0)) 
		
		user = cursor.fetchone()
		
		#user in DB  or not
		if user is not None :
			return True
		else:
			return False
			
	except Exception as e :
		print('error during select : ', e)
		return False
		
	finally:
		CloseDB()

def InsertClients(clients):
    try:
        if(DBConnect() != True): return False

        if len(clients) != 0:
            cmd = '''INSERT OR IGNORE INTO Client (RFID, firstName, slot) VALUES(?, ?, ?)'''
            print('I will insert new commers into local DB')
            for client in clients:
                cursor.execute(cmd, (client[0], client[1], client[2]))
            conn.commit()
        return True

    except Exception as e:
        print('insert error ', e)
        return False
    finally:
        CloseDB()
        

def DeleteClient(rfid, slot):
    try:
        while(DBConnect() != True):
                time.sleep(4)
        
        cmd = '''DELETE FROM Client WHERE RFID = ? AND slot = ?'''
        cursor.execute(cmd, (rfid, slot))
        conn.commit()
        return True
    
    except Exception as e:
        print('delete error ', e)
        return False
    
    finally:
        CloseDB()
        
def changeState(rfid):
    try:
        if(DBConnect() != True): return False
        
        cursor.execute("UPDATE Client SET state = ? WHERE RFID = ?", (1, rfid))
        conn.commit()
        
    except Exception as e :
        print('error during update : ', e)

    finally:
        CloseDB()

def isInside(rfid, slot):
        
        while(DBConnect() != True):
                time.sleep(4)

        cursor.execute("SELECT * FROM Client WHERE RFID = ? AND state = ? AND slot = ?", (rfid, 1, slot))
        
        if cursor.fetchone() is not None :
                return '1'
        else :
                return '0'
        
        

