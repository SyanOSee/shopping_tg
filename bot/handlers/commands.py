# Third-party
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

# Project
import bot.keyboards as kb
import bot.strings as strings
from database.models import User
from modules import database

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    """
    Handler for the '/start' command.
    Sends a greeting message and inserts the user into the database if not already present.
    """
    await message.answer(strings.ru['greeting_msg'], reply_markup=kb.menu_keyboard, parse_mode='html')
    await database.user.insert_if_not_exist(User().init_values(message.from_user.id))


@router.message(F.text)
async def menu_keyboard_handler(message: Message):
    """
    Handler for processing text messages based on the menu keyboard options.
    """
    # Check the message text and execute corresponding actions
    if message.text == strings.ru['about_name']:
        await message.answer(strings.ru['about_msg'], parse_mode='html')
    elif message.text == strings.ru['faq_name']:
        await message.answer(strings.ru['faq_msg'], parse_mode='html')
    elif message.text == strings.ru['cart_name']:
        await handle_cart(message)
    elif message.text == strings.ru['choose_product_name']:
        await handle_choose_product(message)
    elif message.text == strings.ru['payment_name']:
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
                    msg, keyboard = await strings.ru['cart_msg'](category=category, product_info=product_info,
                                                                 product=product)
                    await message.answer(msg, reply_markup=keyboard, parse_mode='html')
    else:
        await message.answer(strings.ru['empty_cart_msg'], parse_mode='html')


async def handle_payment(message: Message):
    """
    Handler for processing payment messages.
    Sends a message with payment options.
    """
    msg, keyboard = strings.ru['choose_payment_msg'], await kb.get_payment_keyboard()
    await message.answer(msg, reply_markup=keyboard, parse_mode='html')


async def handle_choose_product(message: Message):
    """
    Handler for processing product selection messages.
    Sends a message with category options or empty catalogue message if no categories are available.
    """
    categories = await database.product.fetch_categories()
    if categories:
        msg, keyboard = strings.ru['choose_category_msg'], await kb.get_categories_keyboard(categories)
        await message.answer(text=msg, reply_markup=keyboard, parse_mode='html')
    else:
        await message.answer(strings.ru['empty_catalogue_msg'], parse_mode='html')
