from aiogram import types

import utils.constants as cn
from init_loader import dp, bot, db, logger

# CallbackQuery is always str type
async def __process_callback_data(callback_data) -> tuple:
    result = callback_data.replace("data:", "").replace("[", "").replace("]", "").replace("'", "")
    return tuple(result.split(", "))

@dp.callback_query_handler(lambda query: "data" in query.data)
async def handle_callback(callback_query: types.CallbackQuery):
    await logger.info("HANDLE CALLBACK")
    await bot.answer_callback_query(callback_query.id)
    data = await __process_callback_data(callback_query.data)
