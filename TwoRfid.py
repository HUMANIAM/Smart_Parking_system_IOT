#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
from module.MFRC522 import MFRC522
from module.pinos import PinoControle
import time

class Nfc522(object):
    
    pc = PinoControle()
    MIFAREReader = None
    RST1 = 22 #GPIO
    RST2 = 22 #GPIO
    SPI_DEV0 = '/dev/spidev0.0'
    SPI_DEV1 = '/dev/spidev0.1'
    
    def obtem_nfc_rfid(self):
        try:
            self.MIFAREReader = MFRC522(self.RST1, self.SPI_DEV0)
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            
            if status == self.MIFAREReader.MI_OK:
                gid1 =  self.obtem_tag(uid)
            else:
                self.pc.atualiza(self.RST1, self.pc.baixo())
                gid1 = 0
            
        except Exception as e:
            print (e)
            
        try:    
            self.MIFAREReader = MFRC522(self.RST2, self.SPI_DEV1)
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
                
            if status == self.MIFAREReader.MI_OK:
                
                gid2= self.obtem_tag(uid)
            else:
                self.pc.atualiza(self.RST2, self.pc.baixo())
                gid2=0
            

        except Exception as e:
            print (e)


        return gid1,gid2
			
    def obtem_tag(self, uid):
        try:
            tag_hexa = ''.join([str(hex(x)[2:4]).zfill(2) for x in uid[:-1][::-1]]) #Returns in hexadecimal
            return int(tag_hexa.upper(), 16) #Returns in decimal
        except Exception as e:
            print (e)
