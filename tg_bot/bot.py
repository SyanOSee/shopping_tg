# Third-party
from aiogram import Bot, Dispatcher

# Standard
import asyncio

# Project
import tg_bot.config as cf
from tg_bot.logger import Logger


class TelegramBot:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.bot = Bot(cf.bot['token'])
        self.dispatcher = Dispatcher(bot=self.bot, loop=asyncio.get_event_loop())
        self.logger.info('Bot is created')

    def set_routers(self, routers):
        [self.dispatcher.include_router(router) for router in routers]

    async def start(self):
        self.logger.clear_log_file()
        await self.dispatcher.start_polling(self.bot)
