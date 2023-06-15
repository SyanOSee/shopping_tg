from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.constants import ButtonNames

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
menu_buttons = [
    KeyboardButton(ButtonNames.ABOUT),
    KeyboardButton(ButtonNames.FAQ),
    KeyboardButton(ButtonNames.BASKET),
    KeyboardButton(ButtonNames.CHOOSE_PRODUCT),
]
menu_keyboard.add(*menu_buttons)