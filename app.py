from aiogram.types import Update
from fastapi import FastAPI
from aiogram import Dispatcher, Bot

from bot.handlers import dp
from init_loader import logger, bot, cf

app = FastAPI()

# Handle incoming updates via FastAPI route
@app.post(cf.WEBHOOK_PATH)
async def handle_webhook(update: dict):
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    update = Update(**update)
    await dp.process_update(update)

# Set up the startup and shutdown handlers
@app.on_event('startup')
async def on_startup():
    await logger.warning("BOT STARTUP")
    await logger.clear_log_file()
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != cf.BASE_URL + cf.WEBHOOK_PATH:
        await bot.set_webhook(cf.BASE_URL + cf.WEBHOOK_PATH)

@app.on_event('shutdown')
async def on_shutdown():
    await logger.warning("BOT SHUTDOWN")
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    import uvicorn
    # Start the bot using uvicorn server
    uvicorn.run(
        'app:app',
        host=cf.BASE_URL,
        port=8080,
        reload=True,
        log_level='info'
    )