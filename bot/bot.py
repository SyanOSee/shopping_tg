# Third-party
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Standard
import asyncio

# Project
import config as cf
from logger import Logger


class TelegramBot:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.bot = Bot(cf.bot['token'])
        self.dispatcher = Dispatcher(
            bot=self.bot,
            loop=asyncio.get_event_loop(),
            storage=MemoryStorage()
        )
        self.logger.info('Bot is created')

    async def __on_startup(self):
        self.logger.warning("Bot is started")
        self.logger.clear_log_file()

    async def __on_shutdown(self):
        self.logger.warning("Bot is stopped")
        await self.dispatcher.storage.close()
        await self.dispatcher.storage.wait_closed()

    async def start(self):
        executor.start_polling(
            dispatcher=self.dispatcher,
            on_startup=self.__on_startup,
            on_shutdown=self.__on_shutdown,
            skip_updates=True
        )
