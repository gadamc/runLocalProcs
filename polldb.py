#!/usr/bin/env python
from couchdbkit import Server, Database, Consumer
from KDataPy.scripts.dataprocess import runProc0

import datetime
import json
import time

def callback(inputLine):
    n = datetime.datetime.now()
    print ''
    print n
    print json.dumps(inputLine,indent=1)
    print 'waiting for ten minutes before starting data transfer to be sure that the entire data file has been copied to the local disk. We do this because we depend upon the ana scripts that copy data from the samba machines to S7'
    time.sleep(600)
    print ''
    runProc0.main('https://edelweissuser:edwdbw1mp@edelweiss.cloudant.com', 'datadb', 'gadamc','h8z@mqFF12')

def main():
    s = Server('https://edelweissuser:edwdbw1mp@edelweiss.cloudant.com')
    db = s['datadb']
    c = Consumer(db)

    #start listening since = current update sequence.
    #callback function is run.main
    #heartbeat every minute to keep the connection alive.
    c.wait(callback, since = db.info()['update_seq'], filter='proc/newproc0', feed='continuous', heartbeat=60000)  

if __name__ == '__main__':
    main()
