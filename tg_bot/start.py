# Standard
import asyncio

# Project
from handlers.callbacks import callback_router
from handlers.commands import commands_router
from modules import bot


async def start_up_bot():
    bot.set_routers([callback_router, commands_router])
    await bot.start()


if __name__ == '__main__':
    asyncio.run(start_up_bot())
