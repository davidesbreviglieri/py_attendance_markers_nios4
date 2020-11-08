#!/usr/bin/env python
# -*- coding: utf-8 -*-

#======================================================
#DATA CLASS NIOS4
#======================================================

import uuid
import datetime
import sqlite3
import os

def tid():
    #create tid
    return datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')

class data:

    def __init__(self,dbname):
        self.__dbpath = os.path.abspath(os.getcwd()) + "/db/" + dbname + ".sqlite3"

    def getuser(self,rfid_code):

        conn = sqlite3.connect(self.__dbpath)
        c = conn.cursor()
        c.execute("SELECT gguid,name,mail FROM [users] WHERE rfid_code='" + rfid_code + "'")
        records = c.fetchall()
        v = {}
        v["gguid_user"] = ""
        v["name_user"] = ""
        v["mail_user"] = ""

        for r in records:
            v["gguid_user"] = r[0]
            v["name_user"] = r[1]
            v["mail_user"] = r[2]
        
        conn.close()

        return v


    def writedata(self,gguid_user,name_user,mail_user):
        #write data in db
        sqlstring = "INSERT INTO readings("
        sqlstring = sqlstring + "gguid," #0
        sqlstring = sqlstring + "tid," #1
        sqlstring = sqlstring + "eli," #2
        sqlstring = sqlstring + "arc," #3
        sqlstring = sqlstring + "ut," #4
        sqlstring = sqlstring + "uta," #5
        sqlstring = sqlstring + "exp," #6
        sqlstring = sqlstring + "gguidp," #7
        sqlstring = sqlstring + "ind," #8
        sqlstring = sqlstring + "tap," #9
        sqlstring = sqlstring + "dsp," #10
        sqlstring = sqlstring + "dsc," #11
        sqlstring = sqlstring + "dsq1," #12
        sqlstring = sqlstring + "dsq2," #13
        sqlstring = sqlstring + "utc," #14
        sqlstring = sqlstring + "tidc," #15
        sqlstring = sqlstring + "name_user," #16
        sqlstring = sqlstring + "date_read," #17
        sqlstring = sqlstring + "mail_user," #18
        #----------------------------------
        sqlstring = sqlstring[:-1] + ")"
        #----------------------------------
        sqlstring = sqlstring + " VALUES('" + str(uuid.uuid1()) + "'," #0
        sqlstring = sqlstring + tid() + "," #1
        sqlstring = sqlstring + "0," #2
        sqlstring = sqlstring + "0," #3
        sqlstring = sqlstring + "'admin'," #4
        sqlstring = sqlstring + "''," #5
        sqlstring = sqlstring + "''," #6
        sqlstring = sqlstring + "'" + gguid_user + "'," #7
        sqlstring = sqlstring + "0," #8
        sqlstring = sqlstring + "'users'," #9
        sqlstring = sqlstring + "''," #10
        sqlstring = sqlstring + "''," #11
        sqlstring = sqlstring + "0," #12
        sqlstring = sqlstring + "0," #13
        sqlstring = sqlstring + "'admin'," #14
        sqlstring = sqlstring + tid() +  "," #15
        sqlstring = sqlstring + "'"  + name_user + "'," #16
        sqlstring = sqlstring + tid() +  "," #17
        sqlstring = sqlstring + "'" + mail_user +  "'," #18
        #----------------------------------
        sqlstring =  sqlstring[:-1] + ")"
        #print(sqlstring)
        conn = sqlite3.connect(self.__dbpath)
        c = conn.cursor()
        c.execute(sqlstring)
        conn.commit()
        conn.close()


