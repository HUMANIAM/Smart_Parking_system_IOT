import sqlite3 as sqlite
import json
import sys
import RemotServer

db ='clients.db'
conn = sqlite.connect(db)
cursor = conn.cursor()

#name, slot, rfid 
            
                
try:
	cursor.execute('''CREATE TABLE IF NOT EXISTS Client(
	RFID TEXT primary key not null,
	firstname TEXT,
	slot INTEGER,
	state INTEGER default 0
	)''')
	
	cursor.execute('''CREATE TABLE IF NOT EXISTS SlotLeaving(
	RFID TEXT primary key not null,
	slot INTEGER
	)''')
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

def AllowAccess(rfid, stat):
	name, slot, state = IsReserve(rfid, stat)
	if(state != -2):
		return name, slot, state
	else:
		#get new users
                newUsrs = RemotServer.GetNews()
                InsertClients(newUsrs)
                
                return IsReserve(rfid, state)
                

def IsReserve(rfid, state):
    # -2 means the user not in the DB but -1 means user in the db but not has authentication to access the garage
    try:
        if(DBConnect() != True): return "can't connect to the db", -1
        
        cursor.execute("SELECT * FROM Client WHERE RFID = ? AND state = ?", (rfid, state)) 
        
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
        
        

