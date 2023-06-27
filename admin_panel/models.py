from fastapi import Request

from data.database.models import User, Product, Order
from sqladmin import ModelAdmin


class UserModel(ModelAdmin, model=User):
    column_list = [User.id, User.user_id, User.cart, User.order_ids]
    can_edit = False


class ProductModel(ModelAdmin, model=Product):
    column_list = [
        Product.id, Product.product_id, Product.category,
        Product.name, Product.description, Product.image_url,
        Product.cost, Product.amount, Product.discount
    ]
    can_edit = True


class OrderModel(ModelAdmin, model=Order):
    column_list = [Order.id, Order.order_id, Order.products_info, Order.address, Order.trade_time]
    can_edit = False

