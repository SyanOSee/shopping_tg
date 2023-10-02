# Standard
import asyncio

# Project
from bot.handlers import router
from bot.bot import TelegramBot
from logger import Logger


async def start_up_bot():
    bot = TelegramBot(logger=Logger())
    bot.set_router(router=router)
    await bot.start()


if __name__ == '__main__':
    asyncio.run(start_up_bot())
