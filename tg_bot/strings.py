# Project
from database.db import Database
from database.models import Product


async def get_product_card_info_msg(user_id: int, product: Product, database: Database) -> (str, bool):
    message = f'<b>{product.name}</b>\n\n' \
              f'<b>Описание:</b>\n{product.description}\n\n' \
              f'<b>Количество на складе:</b> {product.amount} шт.\n\n' \
              f'<b>Цена с учетом скидки {product.discount}%</b>: {round(product.cost * ((100 - product.discount) / 100))} руб.'
    should_use_add_to_cart_keyboard = True
    if await database.product.check_in_user_cart(user_id=user_id, product=product):
        message += '\n\n<b>Добавлено в корзину</b>'
        should_use_add_to_cart_keyboard = False

    return message, should_use_add_to_cart_keyboard


async def cart_msg(category: str, product_info: dict, product: Product) -> str:
    total_cost = round(product_info["amount"] * product.cost * ((100 - product.discount) / 100))
    msg = f'Категория: {category}\n' \
          f'Название: {product_info["name"]}\n' \
          f'Количество: {product_info["amount"]} шт. (max: {product.amount})\n' \
          f'Итоговая стоимость со скидкой {product.discount}%: {total_cost} руб.'
    return msg


async def update_cart_msg(init_msg: str, cart_amount: int, total_cost: float, product: Product) -> str:
    msg = init_msg.split('\n')
    msg[2] = f'Количество: {cart_amount} шт. (max: {product.amount})'
    msg[3] = f'Итоговая стоимость со скидкой {product.discount}%: {total_cost} руб.'
    return '\n'.join(msg)


def successful_payment_msg(total_price: float, currency: str) -> str:
    return f'Платеж на сумму <i>{total_price} {currency}</i> прошел <b>успешно</b>\n\n<b>Благодарим за покупку!</b>'


ru = {
    'about_name': 'ℹ️ О нас',
    'faq_name': '❓ FAQ',
    'cart_name': '🛒 Корзина',
    'choose_product_name': '🛏 Выбрать мебель',
    'payment_name': '💸 Оплата',
    'go_back_name': 'Вернуться назад',
    'add_to_cart_name': 'Добавить',
    'remove_from_cart_name': 'Убрать',
    'do_not_spam': 'Не спамить!',
    'greeting_msg': '<b>Приветствую в нашем магазине мебели!</b>',
    'about_msg': '<b>О нас</b>\n'
                 'Мы ведущая компания по производству и продаже высококачественной мебели. Наша цель - '
                 'предоставить нашим клиентам уникальные и функциональные решения для создания комфортного '
                 'в их домах и офисах.\n\n'
                 '<b>Наши преимущества:</b>\n'
                 '  • <i>Широкий ассортимент мебели для любого стиля интерьера</i>\n'
                 '  • <i>Индивидуальный подход к каждому клиенту</i>\n'
                 '  • <i>Высокое качество и надежность наших изделий</i>\n'
                 '  • <i>Опытные дизайнеры и мастера</i>\n'
                 '  • <i>Конкурентные цены и гибкая система скидок</i>\n'
                 '  • <i>Быстрая и надежная доставка</i>\n',
    'faq_msg': '<b>1. Каковы сроки доставки?</b>\n'
               '- Обычно сроки доставки составляют от 3 до 7 рабочих дней, в зависимости от вашего местоположения и '
               'доступности товара.\n\n'
               '<b>2. Могу ли я вернуть или обменять товар?</b>\n'
               '- Да, мы гарантируем политику возврата и обмена. Если вы не полностью удовлетворены приобретенным '
               'товаром, вы можете вернуть его в течение 14 дней со дня покупки.\n\n'
               '<b>3. Есть ли у вас гарантия на продукцию?</b>\n'
               '- Да, мы предоставляем гарантию на нашу продукцию. Срок гарантии может различаться в зависимости от '
               'категории товара.',
    'get_product_card_info_msg': get_product_card_info_msg,
    'back_to_catalogue_msg': 'Вернуться в каталог?',
    'empty_cart_msg': 'Корзина пуста',
    'choose_category_msg': 'Выберите категорию:',
    'empty_catalogue_msg': 'Каталог пуст',
    'cart_msg': cart_msg,
    'update_cart_msg': update_cart_msg,
    'invoice_msg': ('Оплата товара',
                    'Тестовая оплата\n\nAddress 1 -  Номер дома и название улицы\nAddress 2 -  Номер квартиры / '
                    'апартаментов / корпуса (номер квартиры может содержать не только цифры, но и буквы)'),
    'choose_payment_msg': '<b>Выберите способ оплаты</b>',
    'successful_payment_msg': successful_payment_msg,
    'nothing_to_pay': '<b>Нет товара в корзине</b>'
}
