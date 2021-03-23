#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import time
import datetime
from sense_hat import SenseHat

# User Variables
#---------------
DEBUG_MODE = False  # Test sensehat.  Get readings every 5 seconds.  No Data will be saved to sensehat.db
SLEEP_SEC = 300    # seconds between data saves to sqlite database sensehat.db

sense = SenseHat()
sense.clear()

def init_db():
    """Connects to the specific database."""
    con = lite.connect("sensehat.db")
    cur = con.cursor()
    query = """CREATE TABLE IF NOT EXISTS
                    sensehat(epoch INT,
                             humidity REAL,
                             pressure REAL,
                             temp_hum REAL,
                             temp_prs REAL)"""
    cur.execute(query)

if __name__ == "__main__":

    humidity = round(sense.humidity, 1)
    pressure = round(sense.get_pressure(), 2)
    temperature_from_humidity = round(sense.get_temperature(), 1)
    temperature_from_pressure = round(sense.get_temperature_from_pressure(), 1)

    init_db()
    
    if DEBUG_MODE:
        print("Note: DEBUG=True")
        print("Data will NOT be saved to sensehat.db")
        print("Readings every 5 seconds to Test if Sensehat hardware is working OK.")
        print("")
    else:
        print("Saving Data to sensehat.db every %i seconds" % SLEEP_SEC)
    echo('Wait 15 Seconds for sensehat to warm up')
    time.sleep(15)
    while True:
        humidity = round(sense.humidity, 1)
        pressure = round(sense.get_pressure(), 2)
        temperature_from_humidity = round(sense.get_temperature(), 1)
        temperature_from_pressure = round(sense.get_temperature_from_pressure(), 1)

        con = lite.connect("sensehat.db")
        with con:
            print("Timestamp= %s  Percent Hum= %0.2f  Deg C= %0.2f  Bar Press= %0.2f" %
                  (datetime.datetime.now().isoformat(),
                   humidity, temperature_from_humidity, pressure))
            if DEBUG_MODE:
                time.sleep(5)
                continue

            cur = con.cursor()
            command = "INSERT INTO sensehat VALUES(%i,%0.2f,%0.2f,%0.2f,%0.2f)" % (int(
                time.time()), humidity, pressure, temperature_from_humidity, temperature_from_pressure)
            cur.execute(command)
        time.sleep(SLEEP_SEC)
