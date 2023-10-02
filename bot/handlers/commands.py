# Third-party
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

# Project
import bot.keyboards as kb
import bot.strings as strings
from database.models import User
from start import *

commands_router = Router()


@commands_router.message(Command('start'))
async def start(message: Message):
    """
    Handler for the '/start' command.
    Sends a greeting message and inserts the user into the database if not already present.
    """
    await logger.info('Start Command')
    await message.answer(strings.Ru.greeting_msg(), reply_markup=kb.menu_keyboard)
    await database.user.insert_if_not_exist(User().init_values(message.from_user.id))


@commands_router.message(F.text)
async def menu_keyboard_handler(message: Message):
    """
    Handler for processing text messages based on the menu keyboard options.
    """
    await logger.info('Menu Keyboard Handler')
    await logger.info(f'Command - {message.text}')

    # Check the message text and execute corresponding actions
    if message.text == strings.Ru.about_name():
        await message.answer(strings.Ru.about_msg())
    elif message.text == strings.Ru.faq_name():
        await message.answer(strings.Ru.faq_msg())
    elif message.text == strings.Ru.cart_name():
        await handle_cart(message)
    elif message.text == strings.Ru.choose_product_name():
        await handle_choose_product(message)
    elif message.text == strings.Ru.payment_name():
        await handle_payment(message)


async def handle_cart(message: Message):
    """
    Handler for processing cart messages.
    Retrieves the user's cart from the database and sends cart information or empty cart message.
    """
    user = await database.user.get_by_id(user_id=message.from_user.id)
    if user.cart:
        for category in await database.product.fetch_categories():
            if category in user.cart:
                for product_info in user.cart[category]:
                    product = await database.product.get_by_id(product_id=product_info['product_id'])
                    msg, keyboard = await strings.Ru.cart_msg(category=category, product_info=product_info,
                                                              product=product)
                    await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer(strings.Ru.empty_cart_msg())


async def handle_payment(message: Message):
    """
    Handler for processing payment messages.
    Sends a message with payment options.
    """
    msg, keyboard = strings.Ru.choose_payment_msg(), await kb.get_payment_keyboard()
    await message.answer(msg, reply_markup=keyboard)


async def handle_choose_product(message: Message):
    """
    Handler for processing product selection messages.
    Sends a message with category options or empty catalogue message if no categories are available.
    """
    categories = await database.product.fetch_categories()
    if categories:
        msg, keyboard = strings.Ru.choose_category_msg(), await kb.get_categories_keyboard(categories)
        await message.answer(text=msg, reply_markup=keyboard)
    else:
        await message.answer(strings.Ru.empty_cart_msg())
