# Third-party
from aiogram import Router, F
from aiogram.types import *

# Project
from handlers.callback_data import *
import keyboards as kb
import format as fmt
from handlers.commands import handle_choose_product
from modules import bot, database
from handlers.middleware import *
from database.models import Order
import config as cf

callback_router = Router()
callback_router.callback_query.middleware(LoggingMiddleware())


@callback_router.callback_query(CategoryCallback.filter())
async def handle_category_callback(callback: CallbackQuery, callback_data: CategoryCallback):
    """
    Callback handler for category selection.
    Retrieves products by category, generates and sends product cards,
    and provides an option to go back to the catalog.
    """
    logger.info('Handling category callback')
    await bot.bot.answer_callback_query(callback.id)
    await callback.message.delete()

    for product in await database.product.get_by_category(callback_data.category):
        # Retrieve message and reply markup for the product card
        msg, should_use_add_to_cart_keyboard = await fmt.ru_strs['get_product_card_info_msg'](
            user_id=callback.from_user.id,
            product=product,
            database=database
        )
        # Send the product card photo message
        if should_use_add_to_cart_keyboard:
            keyboard = await kb.get_add_to_cart_keyboard(product=product)
        else:
            keyboard = await kb.get_remove_from_cart_keyboard(product=product, in_cart=False)
        await bot.bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=product.image_url,
            caption=msg,
            reply_markup=keyboard,
            parse_mode='html'
        )

    # Send a message with an option to go back to the catalog
    await bot.bot.send_message(
        chat_id=callback.message.chat.id,
        text=fmt.ru_strs['back_to_catalogue_msg'],
        reply_markup=await kb.get_back_to_categories_keyboard(),
        parse_mode='html'
    )


@callback_router.callback_query(BackToCatalogueCallback.filter())
async def handle_back_to_catalogue_callback(callback: CallbackQuery):
    """
    Callback handler for going back to catalogue.
    Deletes previously sent messages and invokes the handler to choose a product.
    """
    logger.info('Handling back to categories callback')
    await bot.bot.answer_callback_query(callback.id)

    await callback.message.delete()

    # Invoke the handler to choose a product
    await handle_choose_product(callback.message)


@callback_router.callback_query(AddToCartCallback.filter())
async def handle_add_to_cart_callback(callback: CallbackQuery, callback_data: AddToCartCallback):
    """
    Callback handler for adding a product to the cart.
    """
    logger.info('Handling add to cart data callback')
    product_id = callback_data.product_id
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
    await bot.bot.answer_callback_query(callback.id)
    msg, should_use_add_to_cart_keyboard = await fmt.ru_strs['get_product_card_info_msg'](
        user_id=user.user_id,
        product=product,
        database=database
    )
    if should_use_add_to_cart_keyboard:
        keyboard = await kb.get_add_to_cart_keyboard(product=product)
    else:
        keyboard = await kb.get_remove_from_cart_keyboard(product=product, in_cart=False)
    await callback.message.edit_caption(caption=msg, reply_markup=keyboard, parse_mode='html')


@callback_router.callback_query(RemoveFromCartCallback.filter())
async def handle_remove_from_cart_callback(callback: CallbackQuery, callback_data: RemoveFromCartCallback):
    """
    Callback handler for removing a product from the cart.
    """
    logger.info('Handling remove from cart callback')
    product_id = callback_data.product_id
    in_cart = callback_data.in_cart
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
    await bot.bot.answer_callback_query(callback.id)
    if in_cart:
        await callback.message.delete()
    else:
        msg, should_use_add_to_cart_keyboard = await fmt.ru_strs['get_product_card_info_msg'](
            user_id=user.user_id,
            product=product,
            database=database
        )
        if should_use_add_to_cart_keyboard:
            keyboard = await kb.get_add_to_cart_keyboard(product=product)
        else:
            keyboard = await kb.get_remove_from_cart_keyboard(product=product, in_cart=False)
        await callback.message.edit_caption(caption=msg, reply_markup=keyboard, parse_mode='html')


@callback_router.callback_query(ChangeAmountCallback.filter())
async def handle_change_amount_callback(callback: CallbackQuery, callback_data: ChangeAmountCallback):
    """
    Callback handler for changing the amount of a product in the cart.
    """
    logger.info('Handling change amount callback')
    product_id = callback_data.product_id
    category = callback_data.category
    cart_amount = callback_data.cart_amount
    is_adding = callback_data.is_adding

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

    await bot.bot.answer_callback_query(callback.id)
    msg = await fmt.ru_strs['update_cart_msg'](callback.message.text, cart_amount, total_cost, product)
    await callback.message.edit_text(msg, reply_markup=await kb.get_cart_options_keyboard(
        product_id=product.product_id,
        category=product.category,
        cart_amount=cart_amount,
        in_cart=True,
    ), parse_mode='html')


@callback_router.callback_query(PaymentCallback.filter())
async def handle_payment_callback(callback: CallbackQuery, callback_data: PaymentCallback):
    """
    Callback handler for processing payment.
    """
    logger.info('Handling payment callback')
    await bot.bot.answer_callback_query(callback.id)

    # Match the payment provider and assign the corresponding provider token
    provider = callback_data.provider
    match provider:
        case 'UKassa':
            provider_token = cf.payment['ukassa']
        case 'Paymaster':
            provider_token = cf.payment['paymaster']
        case _:
            provider_token = ''

    # Prepare the prices for the invoice
    user = await database.user.get_by_id(callback.from_user.id)
    prices = []
    for cat, cat_products in user.cart.items():
        for product in cat_products:
            prices.append(LabeledPrice(
                label=f'{product["name"]} x{product["amount"]}',
                amount=int(product["total_cost"] * 100))
            )

    # Send the invoice to the user
    title, description = fmt.ru_strs['invoice_msg']
    if prices:
        await bot.bot.send_invoice(
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
        await callback.message.answer(fmt.ru_strs['nothing_to_pay'], parse_mode='html')


@callback_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """
    Handler for processing pre-checkout queries.
    """
    logger.info('Pre-checkout')
    await bot.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@callback_router.message(F.successful_payment)
async def successful_payment(message: Message):
    """
    Handler for successful payment.
    """
    from uuid import uuid4
    from datetime import datetime

    logger.info('Payment is successful')

    # Extract payment information from the message
    payment_info = message.successful_payment.model_dump()

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
    await bot.bot.send_message(message.chat.id, fmt.ru_strs['successful_payment_msg'](
        total_price=message.successful_payment.total_amount // 100,
        currency=message.successful_payment.currency
    ), parse_mode='html')
