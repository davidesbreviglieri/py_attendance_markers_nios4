#!/usr/bin/env python
# -*- coding: utf-8 -*-
#================================================================================
#Copyright of Davide Sbreviglieri 2020
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
#================================================================================
#ATTENDANCE MARKERS NIOS4
#================================================================================

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

dbname="dbname" #<-- Insert name of your database

viewer = lcd.viewer()
data = data_nios4.data(dbname)

#--------------------------------------
def tid():
    #create tid
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
                #found the control card who is
                suid = ""
                for u in uid:
                  suid = suid + str(u) + ","
                suid = suid[:-1]
                user = data.getuser(suid)
                if user["gguid_user"] == "":
                    viewer.show("Unknow card",2)
                    #if the card is not recognized then I show the id to be able to register it
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
