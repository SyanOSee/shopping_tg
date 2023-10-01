import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config as cf
from database.database import Database
from utils.logger import Logger

# Telegram Bot
bot = Bot(cf.BOT_TOKEN, parse_mode='html')

# Dispatcher
dp = Dispatcher(
    bot,
    loop=asyncio.get_event_loop(),
    storage=MemoryStorage()
)

# anti-spam function
async def anti_spam(*args, **kwargs):
    await args[0].answer('<b>Спам запрещен!</b>')

# Logging object
logger = Logger(cf.LOGGING_PATH)

# Database
db = Database(logger=logger)