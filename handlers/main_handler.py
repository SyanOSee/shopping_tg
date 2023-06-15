from aiogram import types
from aiogram.dispatcher import FSMContext

from data.database.database import Models
from keyboards.reply_keyboard import menu_keyboard
from init_loader import dp, db, logger, anti_spam
from utils.constants import Messages, ButtonNames

@dp.message_handler(commands=['start'])
@dp.throttled(anti_spam, rate=1)
async def start(message: types.Message):
    await logger.info('Start Command')
    await message.answer(Messages.GREETING, parse_mode='Markdown', reply_markup=menu_keyboard)
    await db.insert_user_if_not_exist(Models.User(message.from_user.id))

@dp.message_handler(content_types=['text'])
@dp.throttled(anti_spam, rate=1)
async def menu_keyboard_handler(message: types.Message):
    await logger.info('Menu Keyboard Handler')
    await logger.info(f'Command - {message.text}')
    match message.text:
        case ButtonNames.ABOUT:
            await message.answer(Messages.ABOUT)
        case ButtonNames.FAQ:
            await message.answer(Messages.FAQ, parse_mode='Markdown')
        case ButtonNames.BASKET:
            user = await db.get_user_by_id(message.from_user.id)
            basket = user.basket
            if basket:
                await message.answer('Не пусто')
            else:
                await message.answer('Пусто')
        case ButtonNames.CHOOSE_PRODUCT:
            await message.answer('sus')
