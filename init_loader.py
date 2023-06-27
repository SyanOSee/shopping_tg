import asyncio
from collections import namedtuple

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config as cf
from data.database.database import Database
from utils.logger import Logger

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
    print(args)
    await args[0].answer('<b>Спам запрещен!</b>', parse_mode='html')

# Logging object
logger = Logger(cf.LOGGING_PATH)

# Database information
DbInfo = namedtuple("DbInfo", ["path"])
db_info = DbInfo(
    path=cf.DATABASE_PATH,
)

# Database
db = Database(info=db_info, logger=logger)