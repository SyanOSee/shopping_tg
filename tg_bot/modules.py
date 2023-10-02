# Project
from logger import Logger
from database.db import Database, Type
from bot import TelegramBot
import config as cf

logger = Logger(logging_path=cf.project['log'])
database = Database(type_=Type.LOCAL, logger=logger)
bot = TelegramBot(logger=logger)