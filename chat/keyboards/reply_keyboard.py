from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.str_resources import *

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
menu_buttons = [
    KeyboardButton(about_name()),
    KeyboardButton(faq_name()),
    KeyboardButton(cart_name()),
    KeyboardButton(choose_product_name()),
    KeyboardButton(payment_name())
]
menu_keyboard.add(*menu_buttons)
