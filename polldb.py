#!/usr/bin/env python
from couchdbkit import Server, Database, Consumer
import KDataPy.scripts.dataprocess.runLocalProcs as rp

import datetime
import json
import strjson
import time
import sys


#sys.argv[1] == credentials file in json format
#should contain 'server', 'database', 'sftp_username', 'sftp_password'
try:
    creds = strjson.load(sys.argv[1])
    creds['ftp'] = True
    print json.dumps(creds, indent=1)

except Exception as e:
    print e
    print 'failed to open credentials file'
    sys.exit(1)

def callback(inputLine):

    print ''
    print str(datetime.datetime.now())
    print json.dumps(inputLine,indent=1)
    #print 'waiting for ten minutes before starting data transfer to be sure that the entire data file has been copied to the local disk. We do this because we depend upon the ana scripts that copy data from the samba machines to S7'
    print 'five minute sleep to ensure data transfer complete'
    time.sleep(300)
    print ''
    rp.run(**creds)

s = Server(creds['server'])
db = s[creds['database']]
c = Consumer(db)
print 'starting continuous polling....'
c.wait(callback, since = db.info()['update_seq'], filter='proc/newProc0orMetaProc0', feed='continuous', heartbeat=60000)  

#if we want to be conservative, we can switch to only running when a new log file shows up. comment the line above and uncomment the line below

#c.wait(callback, since = db.info()['update_seq'], filter='proc/newdaqlogfile', feed='continuous', heartbeat=60000)  
