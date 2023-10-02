# Standard
import asyncio

# Project
from tg_bot.handlers.callbacks import callback_router
from tg_bot.handlers.commands import commands_router
from tg_bot.modules import bot


async def start_up_bot():
    bot.set_routers([callback_router, commands_router])
    await bot.start()


if __name__ == '__main__':
    asyncio.run(start_up_bot())
