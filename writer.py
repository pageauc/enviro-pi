#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
PROG_VER = "1.2"

import os
# Get information about this script including name, launch path, etc.
# This allows script to be renamed or relocated to another directory
mypath = os.path.abspath(__file__)  # Find the full path of this python script
# get the path location only (excluding script name)
base_dir = mypath[0:mypath.rfind("/")+1]
prog_filepath = mypath[mypath.rfind("/")+1:mypath.rfind(".")]
PROG_NAME = os.path.basename(__file__)
horz_line = "----------------------------------------------------------------------"

import sys
import time
import datetime
import sqlite3 as lite
from sense_hat import SenseHat
try:
    sense = SenseHat()
except OSError as err_msg:
    print("ERROR - Problem accessing sense hat. Investigate ...")
    print("        %s" % err_msg)
    print("Please investigate problem. Exiting %s ver %s" % (PROG_NAME, PROG_VER))
    sys.exit(1)

config_file_path = os.path.join(base_dir, "config.py")
if os.path.exists(config_file_path):
    # Read Configuration variables from config.py file
    try:
        from config import *
    except ImportError:
        print("WARN  : Problem reading configuration variables from %s" % config_file_path)
else:
    print("ERROR: Missing config.py file - File Not Found %s" % config_file_path)
    print("Please investigate problem. Exiting %s ver %s" % (PROG_NAME, PROG_VER))
    sys.exit(1)

# Initialize variables
writer_db_path = os.path.join(WRITER_DB_DIR, WRITER_DB_NAME)
print(horz_line)
if DEBUG_ON:
    print("%s ver %s  written by Pavol Odlevak and Claude Pageau" % (PROG_NAME, PROG_VER))
    print("Read/Save Humidity, Temperature and Barometric Pressure data to a sqlite3 database.")
else:
    print("Debug = %s" % DEBUG_ON)
    print("Note: nano Edit config file at %s to Enable DEBUG_ON variable" % config_file_path)
    print("SenseHat data will be saved to Sqlite3 Database at %s" %writer_db_path)
print(horz_line)
print("Ctrl-c to Exit ...")

def init_db():
    """Connects to the specific database."""
    con = lite.connect(writer_db_path)
    cur = con.cursor()
    query = """CREATE TABLE IF NOT EXISTS
                    sensehat(epoch INT,
                             humidity REAL,
                             pressure REAL,
                             temp_hum REAL,
                             temp_prs REAL)"""
    cur.execute(query)
    if not os.path.exists(writer_db_path):
        print("ERROR: Could Not Find sqlite3 database at %s" % writer_db_path)
        print("Please Investigate Problem. Exiting %s ver %s" % (PROG_NAME, PROG_VER))
        sys.exit(1)

if __name__ == "__main__":

    # Read data from sensehat
    humidity = round(sense.humidity, 1)
    pressure = round(sense.get_pressure(), 2)
    temperature_from_humidity = round(sense.get_temperature(), 1)
    temperature_from_pressure = round(sense.get_temperature_from_pressure(), 1)

    init_db()  # Initialize the sqlite database

    if DEBUG_ON:
        print("Setting DEBUG_MODE = True")
        print("Data will NOT be saved to sqlite3 database at %s" % writer_db_path)
        print("Reads sensehat every %i sec to Test if hardware is working OK." % DEBUG_SEC)
        print("")
        print("NOTE: To Turn Off Debug Mode")
        print("Edit %s and set DEBUG_ON = False" % config_file_path)
        print("Wait 15 Seconds to Allow SenseHat to Warm Up and avoid erroneous data")
        print(horz_line)
        print("Ctrl-C to Exit Debug")

    time.sleep(15)  # Allow time for sensehat to warm up and avoid erroneous data
    while True:
        humidity = round(sense.humidity, 1)
        pressure = round(sense.get_pressure(), 2)
        temperature_from_humidity = round(sense.get_temperature(), 1)
        temperature_from_pressure = round(sense.get_temperature_from_pressure(), 1)

        con = lite.connect(writer_db_path)
        with con:
            if DEBUG_ON:
                print("Timestamp= %s  Percent Hum= %0.2f  Deg C= %0.2f  Bar Press= %0.2f" %
                      (datetime.datetime.now().isoformat(),
                       humidity, temperature_from_humidity, pressure))
                time.sleep(DEBUG_SEC)
                continue

            cur = con.cursor()
            command = "INSERT INTO sensehat VALUES(%i,%0.2f,%0.2f,%0.2f,%0.2f)" % (
                      int(time.time()), humidity, pressure,
                      temperature_from_humidity, temperature_from_pressure)
            cur.execute(command)
        time.sleep(WRITER_SLEEP_SEC)
