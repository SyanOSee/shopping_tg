# Third-party
from aiogram.types import *

# Project
import strings
import config as cf
from database.models import Order
from commands import handle_choose_product
from start import *


async def __process_callback_data(callback_data) -> str | tuple:
    """
    Process callback data by removing unnecessary characters and returning object or tuple.
    """
    result = callback_data.replace('data:', '').replace('[', '').replace(']', '').replace("'", '').split(', ')
    result[0] = result[0].split('_')[-1]
    if len(result) == 1:
        return result[0]
    else:
        return tuple(result)


@bot.dispatcher.callback_query_handler(lambda query: 'category_data' in query.data)
async def handle_category_callback(callback: CallbackQuery):
    """
    Callback handler for category selection.
    Retrieves products by category, generates and sends product cards,
    and provides an option to go back to the catalog.
    """
    await logger.info('Handling category callback')
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()

    category = await __process_callback_data(callback.data)
    for product in await database.product.get_by_category(category):
        # Retrieve message and reply markup for the product card
        msg, keyboard = await strings.Ru.get_product_card_info_msg(
            user_id=callback.from_user.id,
            product=product
        )
        # Send the product card photo message
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=product.image_url,
            caption=msg,
            reply_markup=keyboard
        )

    # Send a message with an option to go back to the catalog
    msg, keyboard = strings.Ru.back_to_catalogue_msg()
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=msg,
        reply_markup=keyboard
    )


@bot.dispatcher.callback_query_handler(lambda query: 'back_to_catalogue_data' in query.data)
async def handle_back_to_catalogue_callback(callback: CallbackQuery):
    """
    Callback handler for going back to catalogue.
    Deletes previously sent messages and invokes the handler to choose a product.
    """
    await logger.info('Handling back to categories callback')
    await bot.answer_callback_query(callback.id)

    await callback.message.delete()

    # Invoke the handler to choose a product
    await handle_choose_product(callback.message)


@bot.dispatcher.callback_query_handler(lambda query: 'add_to_cart_data' in query.data)
async def handle_add_to_cart_callback(callback: CallbackQuery):
    """
    Callback handler for adding a product to the cart.
    """
    await logger.info('Handling add to cart data callback')
    product_id = int(await __process_callback_data(callback.data))
    product = await database.product.get_by_id(product_id)
    user = await database.user.get_by_id(callback.from_user.id)

    # Add the product to the user's cart
    if product.category not in user.cart:
        user.cart[product.category] = []
    product_ids = [product_info['product_id'] for product_info in user.cart[product.category]]
    if not user.cart[product.category] or product.product_id not in product_ids:
        user.cart[product.category].append({
            'product_id': product.product_id, 'name': product.name,
            'amount': 1, 'total_cost': product.cost * ((100 - product.discount) / 100)
        })
    await database.user.update(user)

    # Update product cards information
    await bot.answer_callback_query(callback.id)
    msg, keyboard = await strings.Ru.get_product_card_info_msg(user.user_id, product)
    await callback.message.edit_caption(caption=msg, reply_markup=keyboard)


@bot.dispatcher.callback_query_handler(lambda query: 'remove_from_cart_data' in query.data)
async def handle_remove_from_cart_callback(callback: CallbackQuery):
    """
    Callback handler for removing a product from the cart.
    """
    await logger.info('Handling remove from cart callback')
    product_id, in_cart = await __process_callback_data(callback.data)
    product_id, in_cart = int(product_id), True if in_cart == 'True' else False
    product, user = await database.product.get_by_id(product_id), await database.user.get_by_id(callback.from_user.id)

    # Remove the product from the user's cart
    for i, product_info in enumerate(user.cart[product.category]):
        if product_info['product_id'] == product_id:
            del user.cart[product.category][i]
            break

    # Remove the category from the user's cart if it becomes empty
    if not user.cart[product.category]:
        del user.cart[product.category]

    await database.user.update(user)
    await bot.answer_callback_query(callback.id)
    if in_cart:
        await callback.message.delete()
    else:
        msg, keyboard = await strings.Ru.get_product_card_info_msg(user.user_id, product)
        await callback.message.edit_caption(caption=msg, reply_markup=keyboard)


@bot.dispatcher.callback_query_handler(lambda query: 'change_amount_data' in query.data)
async def handle_change_amount_callback(callback: CallbackQuery):
    """
    Callback handler for changing the amount of a product in the cart.
    """
    await logger.info('Handling change amount callback')
    product_id, category, cart_amount, is_adding = await __process_callback_data(callback.data)
    product_id, category, cart_amount = int(product_id), category, int(cart_amount)
    is_adding = True if is_adding == 'True' else False

    product = await database.product.get_by_id(product_id)
    user = await database.user.get_by_id(callback.from_user.id)

    # Update the cart amount based on the is_adding flag
    if is_adding and product.amount > cart_amount:
        cart_amount += 1
    elif not is_adding and 1 < cart_amount:
        cart_amount -= 1

    total_cost = round(cart_amount * product.cost * ((100 - product.discount) / 100))
    # Update the cart information for the specific product
    for product_info in user.cart[category]:
        if product_info['product_id'] == product_id:
            product_info['amount'] = cart_amount
            product_info['total_cost'] = total_cost
    await database.user.update(user)

    await bot.answer_callback_query(callback.id)
    msg, keyboard = await strings.Ru.update_cart_msg(callback.message.text, cart_amount, total_cost, product)
    await callback.message.edit_text(msg, reply_markup=keyboard)


@bot.dispatcher.callback_query_handler(lambda query: 'payment_data' in query.data)
async def handle_payment_callback(callback: CallbackQuery):
    """
    Callback handler for processing payment.
    """
    await logger.info('Handling payment callback')
    await bot.answer_callback_query(callback.id)

    # Match the payment provider and assign the corresponding provider token
    provider = await __process_callback_data(callback.data)
    match provider:
        case 'Sberbank':
            provider_token = cf.payment['sber']
        case 'UKassa':
            provider_token = cf.payment['ukassa']
        case _:
            provider_token = ''

    # Prepare the prices for the invoice
    user = await database.user.get_by_id(callback.from_user.id)
    prices = []
    for cat, cat_products in user.cart.items():
        for product in cat_products:
            prices.append(LabeledPrice(f'{product["name"]} x{product["amount"]}', int(product["total_cost"] * 100)))

    # Send the invoice to the user
    title, description = strings.Ru.invoice_msg()
    if prices:
        await bot.send_invoice(
            chat_id=callback.message.chat.id,
            title=title,
            description=description,
            provider_token=provider_token,
            need_shipping_address=True,
            currency='RUB',
            payload='payload',
            prices=prices,
            protect_content=True,
        )
    else:
        await callback.message.answer(strings.Ru.nothing_to_pay())


@bot.dispatcher.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """
    Handler for processing pre-checkout queries.
    """
    await logger.info('Pre-checkout')
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.dispatcher.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    """
    Handler for successful payment.
    """
    from uuid import uuid4
    from datetime import datetime

    await logger.info('Payment is successful')

    # Extract payment information from the message
    payment_info = message.successful_payment.to_python()

    # Fetch order address
    address = ''
    for key, value in payment_info.items():
        if key == 'order_info':
            for address_key, address_value in value['shipping_address'].items():
                address += f'{address_key}: {address_value}\n'

    # Insert the order into the database
    order_id = str(uuid4())
    user = await database.user.get_by_id(message.from_user.id)
    await database.order.insert(Order(
        order_id=order_id,
        products_info=user.cart,
        address=address,
        trade_time=datetime.now().replace(microsecond=0)
    ))

    # Update the product quantities
    for products in user.cart.values():
        for product_info in products:
            product = await database.product.get_by_id(product_info['product_id'])
            product.amount -= product_info['amount']
            await database.product.update(product)

    # Clear the user's cart and update the user in the database
    user.cart = {}
    user.order_ids.append(order_id)
    await database.user.update(user)

    # Send the success message
    await bot.send_message(message.chat.id, strings.Ru.successful_payment_msg(
        total_price=message.successful_payment.total_amount // 100,
        currency=message.successful_payment.currency
    ))
