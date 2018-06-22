import sqlite3 as sqlite
import json
import sys
import RemotServer

#3814746172
db ='clients.db'
conn = sqlite.connect(db)
cursor = conn.cursor()
                
                
try:
	cursor.execute('''CREATE TABLE IF NOT EXISTS Client(
				   RFID TEXT primary key not null,
				   firstname TEXT,
				   slot INTEGER,
				   state INTEGER default 1,
				   accessTime TIMESTAMP  default CURRENT_TIMESTAMP,
				   maxHours FLOAT
				   )
				   ''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS Slot(
				   slot INTEGER primary key not null,
				   state INTEGER default 0
				   )
				   ''')
	conn = sqlite.connect(db)
	cursor = conn.cursor()
	
	for i in range(1, 11):
            cursor.execute('''INSERT OR IGNORE INTO Slot (slot) VALUES(?)''', (i, ))
            
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

def AllowAccess(rfid):
	name, slot, state = IsReserve(rfid)
	if(state != -2):
		return name, slot, state
	else:
		#get new users
                newUsrs = RemotServer.GetNews()
                InsertClients(newUsrs)
                
                return IsReserve(rfid)
                

def IsReserve(rfid):
    # -2 means the user not in the DB but -1 means user in the db but not has authentication to access the garage
    try:
        if(DBConnect() != True): return "can't connect to the db", -1
        
        cursor.execute("SELECT * FROM Client WHERE RFID = ? AND state = 1", (rfid,)) 
        
        user = cursor.fetchone()
        
        #user in DB 
        if user is not None :
                #user in DB
                return user[1], user[2], user[3]
        else:
                return "", -1, -2         #return arbitrary values
        
    except Exception as e :
        print('error during select : ', e)
        return "", -1

    finally:
        CloseDB()

def InsertClients(clients):
    try:
        if(DBConnect() != True): return False

        #get empty slot for the new client
        cursor.execute('SELECT slot FROM Slot WHERE state=0 LIMIT 1')
        emptySlot = cursor.fetchone()[0]

        #change the state of this slot to busy
        cursor.execute("UPDATE Slot SET state = ? WHERE slot = ?", (1, emptySlot))
        conn.commit()
        
        
        cmd = '''INSERT OR IGNORE INTO Client (RFID, firstName, slot, accessTime, maxHours) VALUES(?, ?, ?, ?, ?)'''
        print('I will insert new commers into local DB')
        for client in clients:
            cursor.execute(cmd, (client[0], client[1], emptySlot, client[2], client[3] ))
        conn.commit()
        return True

    except Exception as e:
        print('insert error ', e)
        return False
    finally:
        CloseDB()
        

def DeleteClient(rfid):
    try:
        if(DBConnect() != True): return False
        
        cmd = '''DELETE FROM Client WHERE RFID = ?'''
        cursor.execute(cmd, (rfid,))
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
        
        cursor.execute("UPDATE Client SET state = ? WHERE RFID = ?", (0, rfid))
        conn.commit()
        
    except Exception as e :
        print('error during update : ', e)

    finally:
        CloseDB()

