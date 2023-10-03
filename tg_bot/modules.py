# Project
from tg_bot.logger import Logger
from tg_bot.database.db import Database, Type
from bot import TelegramBot
from admin_panel import config as cf

logger = Logger(logging_path=cf.project['log'])
database = Database(type_=Type.POSTGRESQL, logger=logger)
bot = TelegramBot(logger=logger)