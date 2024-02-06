# configuration settings for enviro-pi.py and weather.py

# Logging Settings
# ----------------
LOGGING_ON = True    # True Enables Logging  False Disables logging

# Weather Underground Settings
# ----------------------------
STATION_UPLOAD_ON = False   # True Enable upload of weather data to Weather Underground
STATION_UPLOAD_MINUTES = 5  # minutes valid values 1 - 60 minutes
STATION_ID = ""             # weather station ID
STATION_KEY = ""            # weather station connection token key

# the weather underground URL used to upload weather data
STATION_WU_URL = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

# SenseHat Settings
# -----------------
SENSEHAT_SCREEN_ON = True     # True = Display status on sense hat LED False = No Display
SENSEHAT_SCREEN_ROTATE = 90   # valid values are 0, 90, 180, 270
SENSEHAT_INIT_MSG = "Enviro"  # Display sensehat LED startup message
SENSEHAT_TEMP_OFFSET = 5.0    # Deg c to correct temperature due to rpi cpu heat

# Sqlite3 Database Settings
# -------------------------
SQLITE3_DB_ON = True              # default= True Write data to Sqlite DB
SQLITE3_DB_NAME = "enviro-pi.db"  # Default="enviro-pi.db" Filename for sqlite3 database
SQLITE3_DB_DIR = "./"             # Default="./"  Directory location for sqlite3 database

# Webserver Settings
# ------------------
WEB_PORT_NUM = 8080        # Default= 8080  Webserver port number