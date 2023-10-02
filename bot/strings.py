# Project
from keyboards import *
from start import database


class Ru:
    @staticmethod
    def about_name() -> str:
        return 'ℹ️ О нас'

    @staticmethod
    def faq_name() -> str:
        return '❓ FAQ'

    @staticmethod
    def cart_name() -> str:
        return '🛒 Корзина'

    @staticmethod
    def choose_product_name() -> str:
        return '🛏 Выбрать мебель'

    @staticmethod
    def payment_name() -> str:
        return '💸 Оплата'

    @staticmethod
    def go_back_name() -> str:
        return 'Вернуться назад'

    @staticmethod
    def add_to_cart_name() -> str:
        return 'Добавить в корзину'

    @staticmethod
    def remove_from_cart_name() -> str:
        return 'Убрать из корзину'

    @staticmethod
    def do_not_spam() -> str:
        return 'Не спамить!'

    @staticmethod
    def greeting_msg() -> str:
        return '<b>Приветствую в нашем магазине мебели!</b>'

    @staticmethod
    def about_msg() -> str:
        return '<b>О нас</b>\n' \
               'Мы ведущая компания по производству и продаже высококачественной мебели. Наша цель - ' \
               'предоставить нашим клиентам уникальные и функциональные решения для создания комфортного ' \
               'в их домах и офисах.\n\n' \
               '<b>Наши преимущества:</b>\n' \
               '  • <i>Широкий ассортимент мебели для любого стиля интерьера</i>\n' \
               '  • <i>Индивидуальный подход к каждому клиенту</i>\n' \
               '  • <i>Высокое качество и надежность наших изделий</i>\n' \
               '  • <i>Опытные дизайнеры и мастера</i>\n' \
               '  • <i>Конкурентные цены и гибкая система скидок</i>\n' \
               '  • <i>Быстрая и надежная доставка</i>\n'

    @staticmethod
    def faq_msg() -> str:
        return '<b>1. Каковы сроки доставки?</b>\n' \
               ' - Обычно сроки доставки составляют от 3 до 7 рабочих дней, в зависимости от вашего местоположения и доступности товара.\n\n' \
               '<b>2. Могу ли я вернуть или обменять товар?</b>\n' \
               ' - Да, мы гарантируем политику возврата и обмена. Если вы не полностью удовлетворены приобретенным товаром, вы можете вернуть его в течение 14 дней со дня покупки.\n\n' \
               '<b>3. Есть ли у вас гарантия на продукцию?</b>\n' \
               ' - Да, мы предоставляем гарантию на нашу продукцию. Срок гарантии может различаться в зависимости от категории товара.'

    @staticmethod
    async def get_product_card_info_msg(user_id: int, product: Product) -> (str, InlineKeyboardMarkup):
        message = f'<b>{product.name}</b>\n\n' \
                  f'<b>Описание:</b>\n{product.description}\n\n' \
                  f'<b>Количество на складе:</b> {product.amount} шт.\n\n' \
                  f'<b>Цена с учетом скидки {product.discount}%</b>: {round(product.cost * ((100 - product.discount) / 100))} руб.'
        keyboard = await get_add_to_cart_keyboard(product)
        if await database.product.check_in_user_cart(user_i=user_id, product=product):
            message += '\n\n<b>Добавлено в корзину</b>'
            keyboard = await get_remove_from_cart_keyboard(product, False)

        return message, keyboard

    @staticmethod
    def back_to_catalogue_msg() -> str:
        return 'Вернуться в каталог?'

    @staticmethod
    def empty_cart_msg() -> str:
        return 'Корзина пуста'

    @staticmethod
    def choose_category_msg() -> str:
        return 'Выберите категорию:'

    @staticmethod
    def empty_catalogue_msg() -> str:
        return 'Каталог пуст'

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def invoice_msg() -> (str, str):
        return 'Оплата товара', 'Тестовая оплата\n\nAddress 1 -  Номер дома и название улицы\nAddress 2 -  Номер квартиры / апартаментов / корпуса (номер квартиры может содержать не только цифры, но и буквы)'

    @staticmethod
    def choose_payment_msg() -> str:
        return '<b>Выберите способ оплаты</b>'

    @staticmethod
    def successful_payment_msg(total_price: float, currency: str) -> str:
        return f'Платеж на сумму <i>{total_price} {currency}</i> прошел <b>успешно</b>\n\n<b>Благодарим за покупку!</b>'

    @staticmethod
    def nothing_to_pay():
        return '<b>Нет товара в корзине</b>'
