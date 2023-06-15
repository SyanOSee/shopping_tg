'''Файл хранит основные объекты, использующиеся в других файлах'''

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from flask import Flask
from pyqiwip2p import QiwiP2P

from collections import namedtuple

import app_config as cf
from utils.logger import Logger
from data.database.database import Database

# Telegram Bot
bot = Bot(cf.BOT_TOKEN)

# Dispatcher
dp = Dispatcher(
    bot,
    loop=asyncio.get_event_loop(),
    storage=MemoryStorage()
)

# anti-spam function
async def anti_spam(*args, **kwargs):
    await args[0].answer("*Спам запрещен!*", parse_mode="MarkdownV2")

# Logging object
logger = Logger(cf.LOGGING_PATH)

# Database information
DbInfo = namedtuple("DbInfo", ["path"])
db_info = DbInfo(
    path=cf.DATABASE_PATH,
)

# Flask server
server = Flask(__name__, template_folder='web/templates')
server.secret_key = cf.FLASK_SECRET_KEY
server.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_info.path}?check_same_thread=False'
server.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Database
db = Database(info=db_info, logger=logger)

# Qiwi
# qiwi = QiwiP2P(auth_key=cf.QIWI_SECRET_TOKEN)