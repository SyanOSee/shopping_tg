from init_loader import logger, dp


# Set up the startup and shutdown handlers
async def on_startup(dp):
    await logger.warning("BOT STARTUP")
    await logger.clear_log_file()


async def on_shutdown(dp):
    await logger.warning("BOT SHUTDOWN")
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    from aiogram.utils.executor import start_polling
    start_polling(dispatcher=dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)