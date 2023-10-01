from data.database.database import Database
from logger import Logger
import config as cf

# Logging object
logger = Logger(cf.LOGGING_PATH)

# Database
db = Database(logger=logger)