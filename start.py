# Standard
import asyncio

# Project
from database.database import Database, Type
from bot.bot import TelegramBot
from logger import Logger
from bot.handlers.commands import commands_router
from bot.handlers.callbacks import callback_router

logger = Logger()
database = Database(type_=Type.LOCAL, logger=logger)
bot = TelegramBot(logger=logger, routers=[commands_router, callback_router])


async def start_up_bot():
    await bot.start()


if __name__ == '__main__':
    asyncio.run(start_up_bot())
