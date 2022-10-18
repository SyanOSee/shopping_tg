'''Файл хранит основные объекты, использующиеся в других файлах'''

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyqiwip2p import QiwiP2P

from collections import namedtuple

import app_config as cf
import utils.constants as cn
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
    await args[0].answer("AntiSpamText", parse_mode="MarkdownV2")

# Logging object
logger = Logger(cf.LOGGING_PATH)

# Database
DbInfo = namedtuple("DbInfo", ["data1", "data2", "etc"])
db_info = DbInfo(
    data1=None,
    data2=None,
    etc=None
)
db = Database(info=db_info, logger=logger)

# Qiwi
qiwi = QiwiP2P(auth_key=cf.QIWI_SECRET_TOKEN)