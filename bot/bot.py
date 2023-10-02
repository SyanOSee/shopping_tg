# Third-party
from aiogram import Bot, Dispatcher

# Standard
import asyncio

# Project
import config as cf
from logger import Logger


class TelegramBot:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.bot = Bot(cf.bot['token'])
        self.dispatcher = Dispatcher(bot=self.bot, loop=asyncio.get_event_loop())
        self.logger.info('Bot is created')

    def set_router(self, router):
        self.dispatcher.include_router(router)

    async def __on_startup(self):
        self.logger.warning("Bot is started")
        self.logger.clear_log_file()

    async def __on_shutdown(self):
        self.logger.warning("Bot is stopped")
        await self.dispatcher.storage.close()

    async def start(self):
        await self.dispatcher.start_polling(self.bot)
