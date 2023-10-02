# Third-party
from aiogram.filters.callback_data import CallbackData


class CategoryCallback(CallbackData, prefix='category'):
    category: str


class BackToCatalogueCallback(CallbackData, prefix='go_back_to_catalogue'):
    blank_: None


class AddToCartCallback(CallbackData, prefix='add_to_cart'):
    product_id: int


class RemoveFromCartCallback(CallbackData, prefix='remove_from_cart'):
    product_id: int
    in_cart: bool


class ChangeAmountCallback(CallbackData, prefix='change_amount'):
    product_id: int
    category: str
    cart_amount: int
    is_adding: bool


class PaymentCallback(CallbackData, prefix='payment_callback'):
    provider: str