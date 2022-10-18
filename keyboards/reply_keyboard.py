from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

example_keyboard = ReplyKeyboardMarkup()
example_buttons = [
    KeyboardButton("Button name")
]

example_keyboard.add(*example_buttons)