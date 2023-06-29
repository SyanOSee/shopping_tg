from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.database.models import Product


async def __go_back_name() -> str:
    return 'Вернуться'


async def __add_to_cart_name() -> str:
    return 'Добавить в корзину'


async def __remove_from_cart_name() -> str:
    return 'Убрать из корзины'


async def get_categories_keyboard(categories: list) -> InlineKeyboardMarkup:
    """1
      Generates an inline keyboard markup with category buttons.
    """
    buttons = []
    for category in categories:
        buttons.append(InlineKeyboardButton(
            category,
            callback_data=CallbackData('category_data', ['category']).new([category])
        ))
    return InlineKeyboardMarkup(row_width=1).add(*buttons)


async def get_back_to_categories_keyboard() -> InlineKeyboardMarkup:
    """
      Generates an inline keyboard markup with back to category button.
    """
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            await __go_back_name(),
            callback_data=CallbackData('back_to_catalogue_data', ['data']).new([None]))
    )


async def get_add_to_cart_keyboard(product: Product) -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard markup with an "Add to Cart" button.
    """
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            await __add_to_cart_name(),
            callback_data=CallbackData('add_to_cart_data', ['product_id']).new([product.product_id])),
    )


async def get_remove_from_cart_keyboard(product: Product, in_cart: bool) -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard markup with a "Remove from Cart" button.
    """
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            await __remove_from_cart_name(),
            callback_data=CallbackData('remove_from_cart_data', ['product_id', 'in_cart']).new(
                [product.product_id, in_cart])),
    )


async def get_cart_options_keyboard(product_id: int, category: str, cart_amount: int,
                                    in_cart: bool) -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard markup with cart options buttons.
    """
    change_amount_callback = CallbackData('change_amount_data', ['product_id', 'category', 'cart_amount', 'is_adding'])
    buttons = [
        InlineKeyboardButton('+', callback_data=change_amount_callback.new(
            [product_id, category, cart_amount, True])),
        InlineKeyboardButton('-', callback_data=change_amount_callback.new(
            [product_id, category, cart_amount, False])),
        InlineKeyboardButton(await __remove_from_cart_name(),
                             callback_data=CallbackData('remove_from_cart_data', ['product_id', 'in_cart']).new(
                                 [product_id, in_cart])),
    ]
    return InlineKeyboardMarkup(row_width=2).add(*buttons)


async def get_payment_keyboard() -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard markup with payment provider buttons.
    """
    buttons = []
    for provider in ['Sberbank', 'UKassa']:
        buttons.append(
            InlineKeyboardButton(provider, callback_data=CallbackData('payment_data', ['provider']).new([provider])))
    return InlineKeyboardMarkup(row_width=1).add(*buttons)
