# Third-party
from sqladmin import ModelView

# Project
from logger import Logger
from database.db import Database, Type
from database.models import User, Product, Order
import config as cf

database = Database(Type.LOCAL, logger=Logger(logging_path=cf.project['log']))


class UserModel(ModelView, model=User):
    column_list = [User.id, User.user_id, User.cart, User.order_ids]
    can_edit = False


class ProductModel(ModelView, model=Product):
    column_list = [
        Product.id, Product.product_id, Product.category,
        Product.name, Product.description, Product.image_url,
        Product.cost, Product.amount, Product.discount
    ]
    can_edit = True


class OrderModel(ModelView, model=Order):
    column_list = [Order.id, Order.order_id, Order.products_info, Order.address, Order.trade_time]
    can_edit = False
