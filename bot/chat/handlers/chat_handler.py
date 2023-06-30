from aiogram.types import *

from init_loader import *
from utils.str_resources import *
from data.database.models import User
from chat.keyboards.reply_keyboard import menu_keyboard


@dp.message_handler(commands=['start'])
@dp.throttled(anti_spam, rate=cf.SPAM_RATE)
async def start(message: Message):
    """
    Handler for the '/start' command.
    Sends a greeting message and inserts the user into the database if not already present.
    """
    await logger.info('Start Command')
    await message.answer(await greeting_msg(), reply_markup=menu_keyboard)
    await db.insert_user_if_not_exist(User().init_values(message.from_user.id))


@dp.message_handler(content_types=['text'])
@dp.throttled(anti_spam, rate=cf.SPAM_RATE)
async def menu_keyboard_handler(message: Message):
    """
    Handler for processing text messages based on the menu keyboard options.
    """
    await logger.info('Menu Keyboard Handler')
    await logger.info(f'Command - {message.text}')

    # Check the message text and execute corresponding actions
    if message.text == about_name():
        await message.answer(await about_msg())
    elif message.text == faq_name():
        await message.answer(await faq_msg())
    elif message.text == cart_name():
        await handle_cart(message)
    elif message.text == choose_product_name():
        await handle_choose_product(message)
    elif message.text == payment_name():
        await handle_payment(message)


async def handle_cart(message: Message):
    """
    Handler for processing cart messages.
    Retrieves the user's cart from the database and sends cart information or empty cart message.
    """
    user = await db.get_user_by_id(message.from_user.id)
    if user.cart:
        for category in await db.get_categories():
            for product_info in user.cart[category]:
                product = await db.get_product_by_id(product_info['product_id'])
                msg, keyboard = await cart_msg(category, product_info, product)
                await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer(await empty_cart_msg())


async def handle_payment(message: Message):
    """
    Handler for processing payment messages.
    Sends a message with payment options.
    """
    msg, keyboard = await choose_payment_msg()
    await message.answer(msg, reply_markup=keyboard)


async def handle_choose_product(message: Message):
    """
    Handler for processing product selection messages.
    Sends a message with category options or empty catalogue message if no categories are available.
    """
    categories = await db.get_categories()
    if categories:
        msg, keyboard = await choose_category_msg(categories)
        await message.answer(text=msg, reply_markup=keyboard)
    else:
        await message.answer(await empty_catalogue_msg())
