# Third-party
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

# Project
import keyboards as kb
import format as fmt
import config as cf
from modules import database
from handlers.middleware import *
from database.models import User
from handlers.states import AdminStates

commands_router = Router()
commands_router.message.middleware(LoggingMiddleware())


@commands_router.message(Command('start'))
async def start(message: Message):
    """
    Handler for the '/start' command.
    Sends a greeting message and inserts the user into the database if not already present.
    """
    await message.answer(fmt.ru_strs['greeting_msg'], reply_markup=kb.menu_keyboard, parse_mode='html')
    await database.user.insert_if_not_exist(User().init_values(message.from_user.id))


@commands_router.message(Command('admin'))
async def admin(message: Message, state: FSMContext):
    """
    Handler for the '/admin' command.
    Asks user to enter name of database
    """
    await message.answer(fmt.ru_strs['admin_enter_username'], parse_mode='html')
    await state.set_state(AdminStates.get_user_name)


@commands_router.message(AdminStates.get_user_name)
async def admin_user_name_state(message: Message, state: FSMContext):
    """
    Handler get_user_name State
    Asks user to enter password of database
    """
    await state.set_data({'admin_name': message.text})
    await message.answer(fmt.ru_strs['admin_enter_password'], parse_mode='html')
    await state.set_state(AdminStates.get_password)


@commands_router.message(AdminStates.get_password)
async def admin_password_state(message: Message, state: FSMContext):
    """
    Handler get_password State
    Asks checks all data and sends url
    """
    user_name, password = (await state.get_data())['admin_name'], message.text
    if user_name == cf.database['user'] and password == cf.database['password']:
        await message.answer(fmt.ru_strs['admin_url'] + f'<b>{cf.server["url"]}</b>', parse_mode='html')
    else:
        await message.answer(fmt.ru_strs['admin_wrong'], parse_mode='html')
    await state.clear()


@commands_router.message(F.text)
async def menu_keyboard_handler(message: Message):
    """
    Handler for processing text messages based on the menu keyboard options.
    """
    # Check the message text and execute corresponding actions
    if message.text == fmt.ru_strs['about_name']:
        await message.answer(fmt.ru_strs['about_msg'], parse_mode='html')
    elif message.text == fmt.ru_strs['faq_name']:
        await message.answer(fmt.ru_strs['faq_msg'], parse_mode='html')
    elif message.text == fmt.ru_strs['cart_name']:
        await handle_cart(message)
    elif message.text == fmt.ru_strs['choose_product_name']:
        await handle_choose_product(message)
    elif message.text == fmt.ru_strs['payment_name']:
        await handle_payment(message)
    else:
        await message.answer(fmt.ru_strs['use_menu_keyboard'], reply_markup=kb.menu_keyboard, parse_mode='html')


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
                    msg = await fmt.ru_strs['cart_msg'](category=category, product_info=product_info,
                                                        product=product)
                    await message.answer(msg, reply_markup=await kb.get_cart_options_keyboard(
                        product_id=product.product_id,
                        category=category,
                        cart_amount=product_info['amount'],
                        in_cart=True
                    ), parse_mode='html')
    else:
        await message.answer(fmt.ru_strs['empty_cart_msg'], parse_mode='html')


async def handle_payment(message: Message):
    """
    Handler for processing payment messages.
    Sends a message with payment options.
    """
    msg, keyboard = fmt.ru_strs['choose_payment_msg'], await kb.get_payment_keyboard()
    await message.answer(msg, reply_markup=keyboard, parse_mode='html')


async def handle_choose_product(message: Message):
    """
    Handler for processing product selection messages.
    Sends a message with category options or empty catalogue message if no categories are available.
    """
    categories = await database.product.fetch_categories()
    if categories:
        msg, keyboard = fmt.ru_strs['choose_category_msg'], await kb.get_categories_keyboard(categories)
        await message.answer(text=msg, reply_markup=keyboard, parse_mode='html')
    else:
        await message.answer(fmt.ru_strs['empty_catalogue_msg'], parse_mode='html')
