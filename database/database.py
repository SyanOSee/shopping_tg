# Third-party
import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# Standard
from time import sleep
from enum import Enum
import traceback

# Project
import config as cf
from logger import Logger
from models import User, Product, Order, base


# Enum for different types of database connections
class Type(Enum):
    LOCAL = f'sqlite:///{cf.database["path"]}'
    REMOTE = f'postgresql://{cf.database["user"]}:{cf.database["password"]}@{cf.database["host"]}:{cf.database["port"]}'


# Class for managing database connections and operations
class Database:
    # Private method to connect to the database
    def __connect_to_database(self, type_: Type, logger: Logger):
        while True:
            self.logger.warning('Connecting to database...')
            try:
                # Creating a database engine
                self.engine = create_engine(type_.value)
                self.session_maker = sessionmaker(bind=self.engine)
                # Creating tables defined in 'base' metadata
                base.metadata.create_all(self.engine)

                # Initializing instances for User, Product, and Order operations
                self.user = self.User(session_maker=sessionmaker, logger=logger)
                self.product = self.Product(session_maker=sessionmaker, logger=logger)
                self.order = self.Order(session_maker=sessionmaker, logger=logger)

                self.logger.info('Connected to database')
                break
            except sqlalchemy.exc.OperationalError:
                # Handling database connection errors
                self.logger.error('Database error:\n' + traceback.format_exc())
                sleep(secs=5)

    # Constructor to initialize the Database class
    def __init__(self, type_: Type, logger: Logger):
        self.logger = logger
        self.__connect_to_database(type_=type_, logger=logger)

    # Class for User operations
    class User:
        def __init__(self, session_maker, logger):
            self.session_maker = session_maker
            self.logger = logger

        # Insert a user if they do not exist in the database
        async def insert_if_not_exist(self, user: User):
            session = self.session_maker()
            db_user = await self.get_by_id(user.user_id)
            if db_user:
                await self.logger.info(f'User {user.user_id} is already in database')
            else:
                session.add(user)
                session.commit()
                await self.logger.info(f'User {user.user_id} is added to database')
            session.close()

        # Delete a user from the database
        async def delete(self, user: User):
            session = self.session_maker()
            session.query(User).filter_by(user_id=user.user_id).delete()
            session.commit()
            await self.logger.warning(f'User {user.user_id} is deleted from database')
            session.close()

        # Get a user by their ID
        async def get_by_id(self, user_id) -> User | None:
            session = self.session_maker()
            data = session.query(User).filter(User.user_id == user_id).first()
            if data:
                await self.logger.info(f'User {user_id} is retrieved from database')
                session.close()
                return data
            else:
                await self.logger.warning(f'User {user_id} is not in database')
                session.close()
                return None

        # Update user information
        async def update(self, user: User):
            session = self.session_maker()
            session.query(User).filter_by(user_id=user.user_id).update({
                'user_id': user.user_id,
                'cart': user.cart,
                'order_ids': user.order_ids
            })
            session.commit()
            await self.logger.info(f'User {user.user_id} is updated')
            session.close()

    # Class for Product operations
    class Product:
        def __init__(self, session_maker, logger):
            self.session_maker = session_maker
            self.logger = logger

        # Check if a product is in a user's cart
        async def check_in_user_cart(self, user_id, product: Product) -> bool:
            session = self.session_maker()
            user = session.query(User).filter_by(user_id=user_id).first()
            if user.cart:
                if product.category in user.cart:
                    product_ids = [product_info['product_id'] for product_info in user.cart[product.category]]
                    return product.product_id in product_ids
            return False

        # Insert a product if it does not exist in the database
        async def insert_if_not_exist(self, product: Product):
            session = self.session_maker()
            db_product = await self.get_by_id(product.product_id)
            if db_product:
                await self.logger.info(f"Product {product.product_id} is already in database")
            else:
                session.add(product)
                session.commit()
                await self.logger.info(f"Product {product.product_id} is added to database")
            session.close()

        # Delete a product from the database
        async def delete(self, product: Product):
            session = self.session_maker()
            session.query(Product).filter_by(product_id=product.product_id).delete()
            session.commit()
            await self.logger.warning(f"Product {product.product_id} is deleted")
            session.close()

        # Get a product by its ID
        async def get_by_id(self, product_id) -> Product | None:
            session = self.session_maker()
            data = session.query(Product).filter(Product.product_id == product_id).first()
            session.close()
            if data:
                await self.logger.info(f"Product {product_id} is retrieved from database")
                return data
            else:
                await self.logger.warning(f"Product {product_id} is not in database")
                return None

        # Get products by category
        async def get_by_category(self, category) -> list | None:
            session = self.session_maker()
            data = session.query(Product).filter(Product.category == category).all()
            session.close()
            if data:
                await self.logger.info(f'Fetched products by category: {category}')
                return data
            else:
                await self.logger.info(f'There are no products with category: {category}')

        # Fetch all product categories
        async def fetch_categories(self) -> list | None:
            session = self.session_maker()
            data = session.query(Product).all()
            session.close()
            if data:
                await self.logger.info('Categories is retrieved')
                return sorted(list(set([product.category for product in data])), key=lambda x: x[0])
            else:
                await self.logger.warning('There are no categories')
                return None

        # Update product information
        async def update(self, product: Product):
            session = self.session_maker()
            session.query(Product).filter_by(product_id=product.product_id).update({
                'category': product.category,
                'name': product.name,
                'description': product.description,
                'image_url': product.image_url,
                'cost': product.cost,
                'amount': product.amount,
                'discount': product.discount
            })
            session.commit()
            await self.logger.info(f'Product {product.product_id} is updated')
            session.close()

    # Class for Order operations
    class Order:
        def __init__(self, session_maker, logger):
            self.session_maker = session_maker
            self.logger = logger

        # Insert an order into the database
        async def insert(self, order: Order):
            session = self.session_maker()
            session.add(order)
            session.commit()
            await self.logger.info(f'Order {order.order_id} inserted in database')
            session.close()

        # Delete an order from the database
        async def delete(self, order: Order):
            session = self.session_maker()
            session.query(Order).filter_by(order_id=order.order_id).delete()
            session.commit()
            await self.logger.warning(f"Order {order.order_id} is deleted")
            session.close()

        # Get an order by its ID
        async def get_by_id(self, order_id) -> Order | None:
            session = self.session_maker()
            data = session.query(Order).filter_by(order_id=order_id).first()
            if data:
                await self.logger.info(f'Order {order_id} is retrieved from database')
                session.close()
                return data
            else:
                await self.logger.warning(f'Order {order_id} not in database')
                session.close()
                return None
