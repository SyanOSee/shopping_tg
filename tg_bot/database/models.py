# Third-party
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import PickleType

# Standard
from datetime import datetime

# Project

# Creating a base class for declarative models
base = declarative_base()


# Defining a User model
class User(base):
    # Specifying the table name
    __tablename__ = 'users'

    # Defining columns and their data types
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True)
    cart = Column(PickleType, default={})
    order_ids = Column(PickleType, default=[])

    # Method to initialize values of the User instance
    def init_values(self, user_id: int, cart=None, order_ids=None):
        if cart is None:
            cart = {}
        if order_ids is None:
            order_ids = []
        self.user_id = user_id
        self.cart = cart
        self.order_ids = order_ids

        return self


# Defining a Product model
class Product(base):
    # Specifying the table name
    __tablename__ = 'products'

    # Defining columns and their data types
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, unique=True)
    category = Column(String)
    name = Column(String)
    description = Column(Text)
    image_url = Column(String)
    cost = Column(Float)
    amount = Column(Integer)
    discount = Column(Integer, default=0)

    # Method to initialize values of the Product instance
    def init_values(self,
                    product_id: int, category: str, name: str,
                    description: str, image_url: str, cost: float,
                    amount: int, discount=0):
        self.product_id = product_id
        self.category = category
        self.name = name
        self.description = description
        self.image_url = image_url
        self.cost = cost
        self.amount = amount
        self.discount = discount

        return self


# Defining an Order model
class Order(base):
    # Specifying the table name
    __tablename__ = 'orders'

    # Defining columns and their data types
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(String, unique=True)
    products_info = Column(PickleType)
    address = Column(String)
    trade_time = Column(DateTime)

    # Method to initialize values of the Order instance
    def init_values(self, order_id: str, products_info: dict,
                    address: str, trade_time: datetime):
        self.order_id = order_id
        self.products_info = products_info
        self.address = address
        self.trade_time = trade_time

        return self
