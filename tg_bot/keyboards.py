# Third-party
from aiogram.utils.keyboard import *

# Project
import format as strings
from database.models import Product
from handlers.callback_data import *

menu_buttons = [
    [KeyboardButton(text=strings.ru_strs['about_name']), KeyboardButton(text=strings.ru_strs['faq_name'])],
    [KeyboardButton(text=strings.ru_strs['cart_name']), KeyboardButton(text=strings.ru_strs['choose_product_name'])],
    [KeyboardButton(text=strings.ru_strs['payment_name'])]
]
menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True, row_width=2)


async def get_categories_keyboard(categories: list) -> InlineKeyboardMarkup:
    """Generates an inline keyboard markup with category buttons"""
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(
            text=category,
            callback_data=CategoryCallback(category=category)
        )
    builder.adjust(1)
    return builder.as_markup()


async def get_back_to_categories_keyboard() -> InlineKeyboardMarkup:
    """Generates an inline keyboard markup with back to category button"""
    return InlineKeyboardBuilder().button(
        text=strings.ru_strs['go_back_name'],
        callback_data=BackToCatalogueCallback(blank_='')
    ).as_markup()


async def get_add_to_cart_keyboard(product: Product) -> InlineKeyboardMarkup:
    """Generates an inline keyboard markup with an "Add to Cart" button"""
    return InlineKeyboardBuilder().button(
        text=strings.ru_strs['add_to_cart_name'],
        callback_data=AddToCartCallback(product_id=product.product_id)
    ).as_markup()


async def get_remove_from_cart_keyboard(product: Product, in_cart: bool) -> InlineKeyboardMarkup:
    """Generates an inline keyboard markup with a "Remove from Cart" button"""
    return InlineKeyboardBuilder().button(
        text=strings.ru_strs['remove_from_cart_name'],
        callback_data=RemoveFromCartCallback(product_id=product.product_id, in_cart=in_cart)
    ).as_markup()


async def get_cart_options_keyboard(product_id: int, category: str,
                                    cart_amount: int, in_cart: bool) -> InlineKeyboardMarkup:
    """Generates an inline keyboard markup with cart options buttons"""
    return InlineKeyboardBuilder().button(
        text='+',
        callback_data=ChangeAmountCallback(product_id=product_id, category=category,
                                           cart_amount=cart_amount, is_adding=True)
    ).button(
        text='-',
        callback_data=ChangeAmountCallback(product_id=product_id, category=category,
                                           cart_amount=cart_amount, is_adding=False)
    ).button(
        text=strings.ru_strs['remove_from_cart_name'],
        callback_data=RemoveFromCartCallback(product_id=product_id, in_cart=in_cart)
    ).as_markup()


async def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Generates an inline keyboard markup with payment provider buttons"""
    builder = InlineKeyboardBuilder()
    for provider in ['UKassa', 'Paymaster']:
        builder.button(
            text=provider,
            callback_data=PaymentCallback(provider=provider)
        )
    builder.adjust(1)
    return builder.as_markup()