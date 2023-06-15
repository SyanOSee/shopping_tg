from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList


class Models:
    base = declarative_base()

    class User(base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(Integer)
        basket = Column(MutableDict.as_mutable(JSON), default={})
        order_ids = Column(MutableList.as_mutable(PickleType), default=[])

        def __init__(self, user_id, basket=None, order_ids=None):
            if basket is None:
                basket = {}
            if order_ids is None:
                order_ids = []
            self.user_id = user_id
            self.basket = basket
            self.order_ids = order_ids

        __table_args__ = (
            CheckConstraint(user_id >= 0, name='positive_value_check'),
        )

    class Product(base):
        __tablename__ = 'products'
        id = Column(Integer, primary_key=True, autoincrement=True)
        product_id = Column(Integer)
        category = Column(String)
        name = Column(String)
        description = Column(Text)
        image_url = Column(String)
        cost = Column(Float)
        amount = Column(Integer)
        discount = Column(Integer, default=0)

        def __init__(self, product_id, category, name, description, image_url, cost, amount, discount=0):
            self.product_id = product_id
            self.category = category
            self.name = name
            self.description = description
            self.image_url = image_url
            self.cost = cost
            self.amount = amount
            self.discount = discount

        __table_args__ = (
            CheckConstraint(product_id >= 0, name='positive_value_check'),
            CheckConstraint(cost >= 0, name='positive_value_check'),
            CheckConstraint(amount >= 0, name='positive_value_check'),
            CheckConstraint(discount >= 0, name='positive_value_check'),
        )

    class Order(base):
        __tablename__ = 'orders'
        id = Column(Integer, primary_key=True, autoincrement=True)
        order_id = Column(Integer)
        products_info = Column(MutableDict.as_mutable(JSON), default={})
        address = Column(String)
        trade_time = Column(DateTime)

        def __init__(self, order_id, products_info, address, trade_time):
            self.order_id = order_id
            self.products_info = products_info
            self.address = address
            self.trade_time = trade_time

        __table_args__ = (
            CheckConstraint(order_id >= 0, name='positive_value_check'),
        )
