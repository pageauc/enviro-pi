#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
PROG_VER = "1.4"

import os
import sys
import platform
import pkg_resources
from sense_hat import SenseHat
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g
from flask import render_template, flash
from flask import send_from_directory
import socket

mypath = os.path.abspath(__file__)  # Find the full path of this python script
# get the path location only (excluding script name)
base_dir = mypath[0:mypath.rfind("/")+1]
config_file_path = os.path.join(base_dir, "config.py")
if os.path.exists(config_file_path):
    # Read Configuration variables from config.py file
    try:
        from config import SQLITE3_DB_NAME, SQLITE3_DB_DIR, WEB_PORT_NUM
    except Exception as err:
        print("ERROR: %s" % err)
        sys.exit(1)
else:
    print("ERROR: File Not Found %s" % config_file_path)
    print("       Investigate problem. Exiting %s " % (PROG_NAME, PROG_VER))
    sys.exit(1)

# Get information about this script including name, launch path, etc.
# This allows script to be renamed or relocated to another directory

prog_filepath = mypath[mypath.rfind("/")+1:mypath.rfind(".")]
PROG_NAME = os.path.basename(__file__)
HORIZ_LINE = "----------------------------------------------------------------------"

# Just a helper variable.
SECONDS_IN_DAY = 86400

# Info for /about requests.
try:
    OS_VERSION = ' '.join(platform.linux_distribution())
except AttributeError:
    import distro
    OS_VERSION = distro.name(pretty=True)

PYTHON_VERSION = platform.python_version()
SENSEHAT_VERSION = pkg_resources.get_distribution("sense_hat").version
FLASK_VERSION = pkg_resources.get_distribution('flask').version

INFO_MESSAGE = '''
<br><br>
Your average in-home relative humidity should be between 40-60% RH percent,
ideally close to 45-50% RH.
<br><br>
Suggested room temperature in winter should be between 20 °C to 23.5 °C and
summer 23 °C to 25.5 °C.
'''

try:
    myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1],
                         [[(s.connect(('8.8.8.8', 53)),
                            s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
                                                                                   socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
except:
    print("ERROR - Can't Find a Network IP Address on this Raspberry Pi")
    print("        Configure Network and Try Again")
    sys.exit(1)

try:
    sense = SenseHat()
except OSError as err_msg:
    print("ERROR - Problem accessing sense hat. Investigate ...")
    print("        %s" % err_msg)
    print("Exit %s ver %s" % (PROG_NAME, PROG_VER))
    sys.exit(1)
sense.clear()

app = Flask(__name__)
# subprocess.check_output(['lsb_release', "-a"]).

app.config.update(dict(
    DATABASE = os.path.join(SQLITE3_DB_DIR, SQLITE3_DB_NAME),
    DEBUG=True
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.route("/charts", methods=['GET', 'POST'])
def show_charts():
    """
    Get date from SQLite and return render_template.
      time_span - sdasdsad
    """
    humidity = []
    pressure = []
    temp_hum = []
    labels = []
    selected_timespan = 'day'
    options = {
        'day': [SECONDS_IN_DAY, 'Last 24 hours'],
        '2day': [SECONDS_IN_DAY * 2, 'Last 2 days'],
        'week': [SECONDS_IN_DAY * 7, 'Last 7 days'],
        'month': [SECONDS_IN_DAY * 30, 'Last 30 days'],
        '3month': [SECONDS_IN_DAY * 90, 'Last 90 days'],
        '6month': [SECONDS_IN_DAY * 180, 'Last 180 days'],
        'year': [SECONDS_IN_DAY * 365, 'Last 365 days']}

    if request.method == 'POST':
        selected_timespan = str(request.form.get('timespan_select'))

    db = get_db()
    query = """
        SELECT strftime('%%Y-%%m-%%d %%H:%%M', epoch, 'unixepoch', 'localtime') as datetime,
               humidity, pressure, temp_hum
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]

    cur = db.execute(query)

    while True:
        row = cur.fetchone()
        if row == None:
            break
        humidity.append(row["humidity"])
        pressure.append(row["pressure"])
        temp_hum.append(row["temp_hum"])
        labels.append(row["datetime"])

    data = {'labels': labels,
            'humidity': humidity,
            'pressure': pressure,
            'temp_hum': temp_hum}
    print(selected_timespan)
    return render_template('charts.html',
                           selected_timespan=selected_timespan,
                           header_timespan=options[selected_timespan][1],
                           humidity=data['humidity'],
                           pressure=data['pressure'],
                           temp_hum=data['temp_hum'],
                           labels=data['labels'])


@app.route("/statistics", methods=['GET', 'POST'])
def show_statistics():
    """
    Get date from SQLite and return render_template.
      time_span - sdasdsad
    """

    selected_timespan = 'day'
    options = {
        'day': [SECONDS_IN_DAY, 'Last 24 hours'],
        '2day': [SECONDS_IN_DAY * 2, 'Last 2 days'],
        'week': [SECONDS_IN_DAY * 7, 'Last 7 days'],
        'month': [SECONDS_IN_DAY * 30, 'Last 30 days']}

    if request.method == 'POST':
        selected_timespan = str(request.form.get('timespan_select'))

    db = get_db()
    query = """
        SELECT MIN(humidity) as min_humidity,
               strftime('%%d-%%m-%%Y %%H:%%M', epoch, 'unixepoch', 'localtime') as min_humidity_datetime
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    min_humidity = str(round(row["min_humidity"], 1)) + \
        "% RH at " + row["min_humidity_datetime"]

    query = """
        SELECT MAX(humidity) as max_humidity,
               strftime('%%d-%%m-%%Y %%H:%%M', epoch, 'unixepoch', 'localtime') as max_humidity_datetime
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    max_humidity = str(round(row["max_humidity"], 1)) + \
        "% RH at " + row["max_humidity_datetime"]

    query = """
        SELECT AVG(humidity) as avg_humidity
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    avg_humidity = str(round(row["avg_humidity"], 1)) + "% RH"

    query = """
        SELECT MIN(pressure) as min_pressure,
               strftime('%%d-%%m-%%Y %%H:%%M', epoch, 'unixepoch', 'localtime') as min_pressure_datetime
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    min_pressure = str(round(row["min_pressure"], 1)) + \
        " hPa at " + row["min_pressure_datetime"]

    query = """
        SELECT MAX(pressure) as max_pressure,
               strftime('%%d-%%m-%%Y %%H:%%M', epoch, 'unixepoch', 'localtime') as max_pressure_datetime
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    max_pressure = str(round(row["max_pressure"], 1)) + \
        " hPa at " + row["max_pressure_datetime"]

    query = """
        SELECT AVG(pressure) as avg_pressure
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    avg_pressure = str(round(row["avg_pressure"], 1)) + " hPa"

    query = """
        SELECT MIN(temp_hum) as min_temp_hum,
               strftime('%%d-%%m-%%Y %%H:%%M', epoch, 'unixepoch', 'localtime') as min_temp_hum_datetime
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    min_temp_hum = str(round(row["min_temp_hum"], 1)) + \
        " °C at " + row["min_temp_hum_datetime"]

    query = """
        SELECT MAX(temp_hum) as max_temp_hum,
               strftime('%%d-%%m-%%Y %%H:%%M', epoch, 'unixepoch', 'localtime') as max_temp_hum_datetime
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    max_temp_hum = str(round(row["max_temp_hum"], 1)) + \
        " °C at " + row["max_temp_hum_datetime"]

    query = """
        SELECT AVG(temp_hum) as avg_temp_hum
        FROM sensehat
        WHERE epoch BETWEEN (strftime('%%s','now')-%i)
                    AND strftime('%%s','now');
        """ % options[selected_timespan][0]
    cur = db.execute(query)
    row = cur.fetchone()
    avg_temp_hum = str(round(row["avg_temp_hum"], 1)) + " °C"

    return render_template('statistics.html',
                           info=INFO_MESSAGE,
                           selected_timespan=selected_timespan,
                           header_timespan=options[selected_timespan][1],
                           min_humidity=min_humidity,
                           max_humidity=max_humidity,
                           avg_humidity=avg_humidity,
                           min_pressure=min_pressure,
                           max_pressure=max_pressure,
                           avg_pressure=avg_pressure,
                           min_temp_hum=min_temp_hum,
                           max_temp_hum=max_temp_hum,
                           avg_temp_hum=avg_temp_hum)

@app.route("/about")
def about():
    return render_template('about.html',
                           os_version=OS_VERSION,
                           python_version=PYTHON_VERSION,
                           sensehat_version=SENSEHAT_VERSION,
                           flask_version=FLASK_VERSION)


@app.route('/status')
@app.route('/')
def index():
    humidity = round(sense.humidity, 1)
    pressure = round(sense.get_pressure(), 2)
    temperature_from_humidity = round(sense.get_temperature(), 1)
    temperature_from_pressure = round(sense.get_temperature_from_pressure(), 1)

    return render_template('status.html', info=INFO_MESSAGE,
                            humidity=humidity, pressure=pressure,
                            temperature_from_humidity=temperature_from_humidity)


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=WEB_PORT_NUM)

