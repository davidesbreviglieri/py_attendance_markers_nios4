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
#DATA NIOS4
#================================================================================

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
        sqlstring = "INSERT INTO scanning("
        sqlstring = sqlstring + "gguid," #0 id record
        sqlstring = sqlstring + "tid," #1 time of last modification 
        sqlstring = sqlstring + "eli," #2 if record is deleted eli=1
        sqlstring = sqlstring + "arc," #3 index of archive
        sqlstring = sqlstring + "ut," #4 last user who modified
        sqlstring = sqlstring + "uta," #5 users who can view the record
        sqlstring = sqlstring + "exp," #6  numeric expressions
        sqlstring = sqlstring + "gguidp," #7 id of any parent record
        sqlstring = sqlstring + "ind," #8 index 
        sqlstring = sqlstring + "tap," #9 table of any parent record
        sqlstring = sqlstring + "dsp," #10 not defined 
        sqlstring = sqlstring + "dsc," #11 not defined
        sqlstring = sqlstring + "dsq1," #12 not defined
        sqlstring = sqlstring + "dsq2," #13 not defined
        sqlstring = sqlstring + "utc," #14 user who created the record
        sqlstring = sqlstring + "tidc," #15 the date and time when the record was created
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
        conn = sqlite3.connect(self.__dbpath)
        c = conn.cursor()
        c.execute(sqlstring)
        conn.commit()
        conn.close()


