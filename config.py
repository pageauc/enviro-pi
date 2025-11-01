# configuration settings for enviro-pi.py 

# Logging Settings
# ----------------
LOGGING_ON = True    # True Enables Logging  False Disables logging

# mqtt config settings
# --------------------
MQTT_ON = False
MQTT_TOPIC = 'DHT/DHT_SENSEHAT'
MQTT_BROKER = '192.168.1.100'
MQTT_PORT = 1883

# Optional MQTT Credentials
MQTT_LOGIN_ON = False
MQTT_LOGIN = "login"
MQTT_PWD = "password"

SENSOR_ID = 'DHT_SENSEHAT'
SENSOR_LOCATION = 'location of RPI with sensehat'

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
SENSEHAT_TEMP_OFFSET = 3.0    # Deg c to correct temperature due to rpi cpu heat

# Sqlite3 Database Settings
# -------------------------
SQLITE3_DB_ON = True              # default= True Write data to Sqlite DB
SQLITE3_DB_NAME = "enviro_pi.db"  # Default="enviro-pi.db" Filename for sqlite3 database
SQLITE3_DB_DIR = "./data"         # Default="./"  Directory location for sqlite3 database

# Webserver Settings
# ------------------
WEB_PORT_NUM = 8090        # Default= 8080  Webserver port number

