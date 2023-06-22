'''Файл запуска'''
from bot.handlers import dp
from init_loader import logger


async def on_startup(dp):
    await logger.warning("BOT STARTUP")
    await logger.clear_log_file()

async def on_shutdown(dp):
    await logger.warning("BOT SHUTDOWN")
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    # server.run(debug=True)
    from aiogram.utils import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)