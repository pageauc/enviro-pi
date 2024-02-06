#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
PROG_VER = "2.2"
print("Loading Wait ...")
import os
# Get information about this script including name, launch path, etc.
# This allows script to be renamed or relocated to another directory
mypath = os.path.abspath(__file__)  # Find the full path of this python script
# get the path location only (excluding script name)
base_dir = mypath[0:mypath.rfind("/")+1]
prog_filepath = mypath[mypath.rfind("/")+1:mypath.rfind(".")]
PROG_NAME = os.path.basename(__file__)
HORIZ_LINE = "----------------------------------------------------------------------"

print(HORIZ_LINE)
print("%s ver %s written by Pavol Odlevak and Claude Pageau" % (PROG_NAME, PROG_VER))
print("\nRead/Save SenseHat Humidity, Temperature and Barometric Pressure data to a sqlite3 database.")
print("Run webserver.py to View Data History graphs via Web Browser.\n")
print("Optional: Upload data to the Weather Underground Personal Weather Station (PWS)")
print(HORIZ_LINE)

import time
import datetime
import sys
import logging

try:
    import requests
except ImportError:
    import pip._vendor.requests as requests

try:
    import sqlite3 as lite
except ImportError:
    print("Install sqlite3 Python library per below.  Then retry")
    print("sudo apt install sqlite3")
    sys.exit(1)

# Read configuration settings from file
config_file_path = os.path.join(base_dir, "config.py")
if os.path.exists(config_file_path):
    # Read Configuration variables from config.py file
    try:
        from config import *
    except ImportError:
        print("WARN  : Problem reading configuration variables from %s" % config_file_path)
        sys.exit(1)
else:
    print("ERROR: Missing config.py file - File Not Found %s" % config_file_path)
    print("Please investigate problem. Exiting %s ver %s" % (PROG_NAME, PROG_VER))
    sys.exit(1)

if LOGGING_ON:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(funcName)-10s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                       )
else:
    print("WARNING: Logging Disabled per LOGGING_ON = %s" %LOGGING_ON)

# Check that STATION_UPLOAD_MINUTES is not None and  less than 60
if (STATION_UPLOAD_MINUTES is None) or (STATION_UPLOAD_MINUTES > 60):
    logging.error("STATION_UPLOAD_MINUTES= %i Cannot be empty or greater than 60 minutes",
                  STATION_UPLOAD_MINUTES)
    sys.exit(1)

# Load SenseHat and Check for Errors
try:
    from sense_hat import SenseHat
except ImportError:
    print("Install Sense Hat Python library per below.  Then retry")
    print("sudo apt install sense-hat")
    sys.exit(1)
try:
    sense = SenseHat()
except OSError as err_msg:
    print("ERROR - Problem accessing Sense Hat ...")
    print("        %s" % err_msg)
    print("Please investigate problem. Exiting %s ver %s" % (PROG_NAME, PROG_VER))
    sys.exit(1)

# Create path to Sqlite3 Database File
sqlite3_db_path = os.path.join(SQLITE3_DB_DIR, SQLITE3_DB_NAME)

# constants used to display an up and down arrows plus bars and hourglass
# modified from https://www.raspberrypi.org/learning/getting-started-with-the-sense-hat/worksheet/
# set up the colours (blue, green, red, empty)

b = [0, 0, 255]  # blue
g = [0, 255, 0]  # green
r = [255, 0, 0]  # red
e = [0, 0, 0]    # empty

# create images for up and down arrows
arrow_up = [
    e, e, e, r, r, e, e, e,
    e, e, r, r, r, r, e, e,
    e, r, e, r, r, e, r, e,
    r, e, e, r, r, e, e, r,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e
]

arrow_down = [
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    b, e, e, b, b, e, e, b,
    e, b, e, b, b, e, b, e,
    e, e, b, b, b, b, e, e,
    e, e, e, b, b, e, e, e
]

bars = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e
]

hourglass = [
    b, b, b, b, b, b, b, b,
    e, b, b, b, b, b, b, e,
    e, e, b, b, b, b, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, b, b, b, b, e, e,
    e, b, b, b, b, b, b, e,
    b, b, b, b, b, b, b, b
]


#------------------------------------------------------
def init_db():
    """Connects to the specific database."""
    con = lite.connect(sqlite3_db_path)
    cur = con.cursor()
    query = """CREATE TABLE IF NOT EXISTS
                    sensehat(epoch INT,
                             humidity REAL,
                             pressure REAL,
                             temp_hum REAL,
                             temp_prs REAL)"""
    cur.execute(query)
    if not os.path.exists(sqlite3_db_path):
        print("ERROR: Could Not Find sqlite3 database at %s" % sqlite3_db_path)
        print("Please Investigate Problem. Exiting %s ver %s" % (PROG_NAME, PROG_VER))
        sys.exit(1)


#------------------------------------------------------
def c_to_f(input_temp):
    # convert input_temp from Celsius to Fahrenheit
    return (input_temp * 1.8) + 32


#------------------------------------------------------
def get_cpu_temp():
    # 'borrowed' from https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=111457
    # executes a command at the OS to pull in the CPU temperature
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))

#------------------------------------------------------
def get_smooth(x):
    # use moving average to smooth readings

    # do we have the t object?
    if not hasattr(get_smooth, "t"):
        # then create it
        get_smooth.t = [x, x, x]
    # manage the rolling previous values
    get_smooth.t[2] = get_smooth.t[1]
    get_smooth.t[1] = get_smooth.t[0]
    get_smooth.t[0] = x
    # average the three last temperatures
    xs = (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3
    return xs


#------------------------------------------------------
def get_temp():
    # ====================================================================
    # Unfortunately, getting an accurate temperature reading from the
    # Sense HAT is improbable, see here:
    # https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=111457
    # so we'll have to do some approximation of the actual temp
    # taking CPU temp into account. The Pi foundation recommended
    # using the following:
    # http://yaab-arduino.blogspot.co.uk/2016/08/accurate-temperature-reading-sensehat.html
    # ====================================================================
    # First, get temp readings from both sensors
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    # t becomes the average of the temperatures from both sensors
    t = (t1 + t2) / 2
    # Now, grab the CPU temperature
    t_cpu = get_cpu_temp()
    # Calculate the 'real' temperature compensating for CPU heating
    t_corr = t - ((t_cpu - t) / 1.5)
    # Finally, average out that value across the last three readings
    t_corr = get_smooth(t_corr)
    # convoluted, right?
    # Return the calculated temperature
    return t_corr - SENSEHAT_TEMP_OFFSET


#------------------------------------------------------
def main():
    if SQLITE3_DB_ON:
        init_db()  # Initialize the sqlite database
        con = lite.connect(sqlite3_db_path)
    last_temp = get_temp()
    # initialize the lastMinute variable to current time to start
    last_minute = datetime.datetime.now().minute
    # on startup, just use the previous minute as lastMinute
    last_minute -= 1
    if last_minute == 0:
        last_minute = 59

    if STATION_UPLOAD_ON:
       mode = "Upload"
    else:
       mode = "Reading"
    logging.info("Next %s in %i minutes. Waiting ...", mode, STATION_UPLOAD_MINUTES)
    # infinite loop to continuously Read/Upload weather values
    while True:
        # The temp measurement smoothing algorithm's accuracy is based
        # on frequent measurements, so we'll take measurements every 5 seconds
        # but only upload on STATION_UPLOAD_MINUTES
        current_second = datetime.datetime.now().second
        # are we at the top of the minute or at a 5 second interval?
        if (current_second == 0) or ((current_second % 10) == 0):
            # ========================================================
            # read values from the Sense HAT
            # ========================================================
            # calculate the temperature
            calc_temp = get_temp()
            # now use it for our purposes
            temp_c = round(calc_temp, 1)
            temp_f = round(c_to_f(calc_temp), 1)
            humidity = round(sense.get_humidity(), 0)
            # convert pressure from millibars to inHg before posting
            pressure = round(sense.get_pressure() * 0.0295300, 1)
            # get the current minute
            current_minute = datetime.datetime.now().minute
            # is it the same minute as the last time we checked?
            if current_minute != last_minute:
                # reset last_minute to the current_minute
                last_minute = current_minute
                # is minute zero, or divisible by 10?
                # we're only going to take measurements every STATION_UPLOAD_MINUTES minutes
                if (current_minute == 0) or ((current_minute % STATION_UPLOAD_MINUTES) == 0):
                    # Update sqlite3 database
                    logging.info("  READING: Temp: %sF(%sC), Press: %s inHg, Hum: %s%%",
                                 temp_f, temp_c, pressure, humidity)
                    if SQLITE3_DB_ON:
                        logging.info("  SQLITE3: INSERT Data INTO table sensehat at %s", sqlite3_db_path)
                        with con:
                            cur = con.cursor()
                            command = "INSERT INTO sensehat VALUES(%i, %0.2f, %0.2f, %0.2f, %0.2f)" % (
                                      int(time.time()), humidity, pressure, temp_c, pressure)
                            try:
                                cur.execute(command)
                            except Exception as err:
                                logging.error("DB Update Failed: %s\nError: %s", command, str(err))
                    else:
                        logging.warning("  SQLITE3: DB DISABLED per SQLITE3_DB_ON = %s", SQLITE3_DB_ON)
                    now = datetime.datetime.now()
                    # did the temperature go up or down?
                    if SENSEHAT_SCREEN_ON:
                        if temp_f == last_temp:
                            # temperature stayed the same
                            # display red and blue bars
                            sense.set_pixels(bars)                        
                        elif temp_f > last_temp:
                            # display a red, up arrow
                            sense.set_pixels(arrow_up)
                        else:
                            # display a blue, down arrow
                            sense.set_pixels(arrow_down)

                    # set last_temp to the current temperature before we measure again
                    last_temp = temp_f

                    # ========================================================
                    # Upload the weather data to Weather Underground
                    # ========================================================
                    # is weather upload enabled (True)?
                    if STATION_UPLOAD_ON:
                        # From http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
                        # build a weather data object
                        weather_data = {"action": "updateraw",
                                        "ID": STATION_ID,
                                        "PASSWORD": STATION_KEY,
                                        "dateutc": "now",
                                        "tempf": str(temp_f),
                                        "humidity": str(humidity),
                                        "baromin": str(pressure),
                                       }
                        try:
                            logging.info("  CONNECT: Station ID %s", STATION_ID)
                            response = requests.get(STATION_WU_URL, weather_data)
                            html_status = response.text.upper().rstrip('\n')
                            logging.info("  UPLOAD : %s", html_status)
                            if SENSEHAT_SCREEN_ON:
                                if html_status == "SUCCESS":
                                    sense.set_pixel(0, 0, g)
                                else:
                                    sense.set_pixel(0, 0, r)
                        except Exception as err:
                            logging.warning("  %s",err)
                    else:
                        logging.warning("  UPLOAD: Disabled per STATION_UPLOAD_ON = %s",
                                        STATION_UPLOAD_ON)
                    logging.info("Next %s in %i minutes. Waiting ...",
                                  mode, STATION_UPLOAD_MINUTES)

if __name__ == "__main__":
    ########################################
    # Check and Initialize program variables
    ########################################
    try:
        logging.info("CONNECT: senseHat ....")
        sense = SenseHat()
        sense.set_rotation(SENSEHAT_SCREEN_ROTATE)
        # then write some text to the Sense HAT's 'screen'
        sense.show_message(SENSEHAT_INIT_MSG, text_colour=[255, 255, 0], back_colour=[0, 0, 255])
        # clear the screen
        sense.clear()
        if SENSEHAT_SCREEN_ON:
            sense.set_pixels(hourglass)
        # get the current temp to use when checking the previous measurement
        last_temp = round(c_to_f(get_temp()), 1)
    except Exception as err:
        logging.error("CONNECT: %s", err)
        sys.exit(1)

    logging.info("READING: SUCCESS SenseHat OK. Temp is %dF", last_temp)
    try:
        main()
    except KeyboardInterrupt:
        sense.show_message("BYE", text_colour=[255, 255, 0], back_colour=[0, 0, 255])
        time.sleep(2)
        sense.clear()
        print("\nUser Exited with Ctrl-c")
        print("Bye ....")
        sys.exit()