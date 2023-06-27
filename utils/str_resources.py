from bot.keyboards.inline_keyboards import *


def about_name() -> str:
    return 'ℹ️ О нас'


def faq_name() -> str:
    return '❓ FAQ'


def cart_name() -> str:
    return '🛒 Корзина'


def choose_product_name() -> str:
    return '🛏 Выбрать мебель'


def payment_name() -> str:
    return '💸 Оплата'


async def greeting_msg() -> str:
    return '<b>Приветствую в нашем магазине мебели!</b>'


async def about_msg() -> str:
    return 'Наша мебельная компания с городстью предлагает качественную и стильную мебель ' \
           'для вашего дома уже более 25 лет. Мы являемся надежным партнером для тех, кто ' \
           'ценит комфорт, функциональность и эстетику в своем интерьере.\n\n' \
           'За все эти годы мы собрали богатый опыт и укрепили свою репутацию благодаря высокому качеству ' \
           'наших изделий и превосходному обслуживанию клиентов. Мы тщательно выбираем материалы и ' \
           'работаем только с талантливыми мастерами, чтобы предложить вам мебель, которая прослужит долгие годы и подарит вам радость и удовлетворение.'


async def faq_msg() -> str:
    return '<b>1. Каковы сроки доставки?</b>\n' \
           ' - Обычно сроки доставки составляют от 3 до 7 рабочих дней, в зависимости от вашего местоположения и доступности товара.\n\n' \
           '<b>2. Могу ли я вернуть или обменять товар?</b>\n' \
           ' - Да, мы гарантируем политику возврата и обмена. Если вы не полностью удовлетворены приобретенным товаром, вы можете вернуть его в течение 14 дней со дня покупки.\n\n' \
           '<b>3. Есть ли у вас гарантия на продукцию?</b>\n' \
           ' - Да, мы предоставляем гарантию на нашу продукцию. Срок гарантии может различаться в зависимости от категории товара.'


async def get_product_card_info_msg(user_id: int, product: Product) -> (str, InlineKeyboardMarkup):
    from init_loader import db
    message = f'<b>{product.name}</b>\n\n' \
              f'<b>Описание:</b>\n{product.description}\n\n' \
              f'<b>Количество на складе:</b> {product.amount} шт.\n\n' \
              f'<b>Цена с учетом скидки {product.discount}%</b>: {round(product.cost * ((100 - product.discount) / 100))} руб.'
    keyboard = await get_add_to_cart_keyboard(product)
    if await db.check_product_in_user_cart(user_id, product):
        message += '\n\n<b>Добавлено в корзину</b>'
        keyboard = await get_remove_from_cart_keyboard(product, False)

    return message, keyboard


async def back_to_catalogue_msg() -> (str, InlineKeyboardMarkup):
    return 'Вернуться в каталог?', await get_back_to_categories_keyboard()


async def empty_cart_msg() -> str:
    return 'Корзина пуста'


async def choose_category_msg(categories: list) -> (str, InlineKeyboardMarkup):
    return 'Выберите категорию:', await get_categories_keyboard(categories)


async def empty_catalogue_msg() -> str:
    return 'Каталог пуст'


async def cart_msg(category: str, product_info: dict, product: Product) -> (str, InlineKeyboardMarkup):
    total_cost = round(product_info["amount"] * product.cost * ((100 - product.discount) / 100))
    msg = f'Категория: {category}\n' \
          f'Название: {product_info["name"]}\n' \
          f'Количество: {product_info["amount"]} шт. (max: {product.amount})\n' \
          f'Итоговая стоимость со скидкой {product.discount}%: {total_cost} руб.'
    keyboard = await get_cart_options_keyboard(
        product_id=product.product_id,
        category=category,
        cart_amount=product_info['amount'],
        in_cart=True
    )
    return msg, keyboard


async def update_cart_msg(init_msg: str, cart_amount: int, total_cost: float, product: Product) -> (
        str, InlineKeyboardMarkup):
    msg = init_msg.split('\n')
    msg[2] = f'Количество: {cart_amount} шт. (max: {product.amount})'
    msg[3] = f'Итоговая стоимость со скидкой {product.discount}%: {total_cost} руб.'
    keyboard = await get_cart_options_keyboard(
        product_id=product.product_id,
        category=product.category,
        cart_amount=cart_amount,
        in_cart=True
    )
    return '\n'.join(msg), keyboard


async def invoice_msg() -> (str, str):
    return 'Оплата товара', 'Введите необходимые данные'


async def choose_payment_msg() -> (str, InlineKeyboardMarkup):
    return '<b>Выберите способ оплаты</b>', await get_payment_keyboard()


async def successful_payment_msg(total_price: float, currency: str) -> str:
    return f'Платеж на сумму <i>{total_price} {currency}</i> прошел <b>успешно</b>\n\n<b>Благодарим за покупку!</b>'
