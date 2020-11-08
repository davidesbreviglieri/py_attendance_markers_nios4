#!/usr/bin/env python
# -*- coding: utf-8 -*-

#ps aux | grep python
#sudo killall python

import smbus
import socket
import time
import datetime
import RPi.GPIO as GPIO
import lcd
import data_nios4
import MFRC522
import signal
import time
import json
import os
import uuid 

dbname="dbname"

viewer = lcd.viewer()
data = data_nios4.data(dbname)

#--------------------------------------
def tid():
    #estrapolo il tid
    return datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

#===================================================================

def main():

    #------------------------------------------
    #Inizializzo segnaore

    count_ip =0 # count read ip
    count_rfid = 0 #cout read rfid
    count_wrow = 0 #count writerow

    print("START ATTENDANCE MAKERS")
    viewer.show("D-One " + get_ip(),4)
    MIFAREReader = MFRC522.MFRC522()

    read_rfid = True

    while True:

        count_ip = count_ip + 1
        if count_ip > 10:
            viewer.show("D-One " + get_ip(),4)
            count_ip = 0

        count_rfid = count_rfid -1
        if count_rfid < 0:
            count_rfid = 0

        count_wrow = count_wrow -1
        if count_wrow < 0:
            count_wrow = 0
            viewer.show("",2)
            viewer.show("",3)

        time.sleep(0.5)

        viewer.show(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 1)

        #------------------------------------------------------------
        if read_rfid == True and count_rfid == 0:
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                #ho trovato la card e quindi procedo al riconoscimento
                suid = ""
                for u in uid:
                  suid = suid + str(u) + ","
                suid = suid[:-1]
                user = data.getuser(suid)
                if user["gguid_user"] == "":
                    viewer.show("Invalid card",2)
                    viewer.show(suid,3)
                    count_rfid = 1
                    count_wrow = 5
                else:
                    data.writedata(user["gguid_user"],user["name_user"],user["mail_user"])
                    viewer.show("Card of ",2)
                    viewer.show(user["name_user"],3)
                    count_rfid = 1
                    count_wrow = 5

        #------------------------------------------------------------

#===================================================================

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()
    viewer.lcd_byte(0x01, 0)

#--------------------------------------
