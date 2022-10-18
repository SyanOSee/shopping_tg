from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import callbacks.example_callbacks as cb

example_keyboard = InlineKeyboardMarkup()

example_buttons = [
    InlineKeyboardButton(
        "Button Name",
        callback_data=cb.example_callback.new( # Callback type is CallbackData or is str
            ["arg1", "arg2"]
        )
    )
]

example_keyboard.add(*example_buttons)