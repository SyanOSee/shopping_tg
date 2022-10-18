'''Файл сервера'''

from fastapi import FastAPI
from aiogram.types import Update
from aiogram import Bot, Dispatcher

from handlers import dp
from init_loader import bot, logger
from app_config import WEBHOOK_URL, WEBHOOK_PATH

app = FastAPI()

async def __set_webhook():
    await logger.info("SETTING WEBHOOK")
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

@app.on_event('startup')
async def on_startup():
    await logger.warning("BOT STARTUP")
    await logger.clear_log_file()
    await __set_webhook()

@app.on_event('shutdown')
async def on_shutdown():
    await logger.warning("BOT SHUTDOWN")
    await dp.storage.close()
    await dp.storage.wait_closed()

@app.post(WEBHOOK_PATH)
async def handle_updates(update: dict):
    await logger.info("HANDLING UPDATE")
    await logger.info(update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(Update(**update))