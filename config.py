# configuration settings for enviro-pi

# Debug settings
# --------------
DEBUG_ON = False  # Default=False True = Display sensehat debug data  False = Write sensehat data to database
DEBUG_SEC = 5     # Default=5  Delay seconds between debug readings.

# Enviro writer.py Settings
# ----------------------
WRITER_SLEEP_SEC = 300  # Default=300 seconds between sensehat data saves to sqlite database
WRITER_DB_NAME = "sensehat.db"  # Default="sensehat.db" Filename for enviro database
WRITER_DB_DIR = "./"    # Default="./"  Directory location for enviro database
