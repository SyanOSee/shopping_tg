import sqlalchemy.exc

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from time import sleep
import traceback

from data.database.models import User, Product, Order, base
import config as cf


class Database:
    def __init__(self, logger):
        while True:
            print('Connecting...')
            try:
                # self.engine = create_engine(f'postgresql://'
                #                             f'{cf.DATABASE_USER}:{cf.DATABASE_PASSWORD}'
                #                             f'@{cf.DATABASE_HOST}:{cf.DATABASE_PORT}')
                self.engine = create_engine(f"sqlite:///{cf.DATABASE_PATH}")
                self.session_maker = sessionmaker(bind=self.engine)
                self.logger = logger

                base.metadata.create_all(self.engine)
                break
            except sqlalchemy.exc.OperationalError:
                print(traceback.format_exc())
                print('Trying again in 5 sec.')
                sleep(5)

    async def insert_user_if_not_exist(self, user: User):
        session = self.session_maker()
        db_user = await self.get_user_by_id(user.user_id)
        if db_user:
            await self.logger.info(f'User {user.user_id} is already in database')
        else:
            session.add(user)
            session.commit()
            await self.logger.info(f'User {user.user_id} is added to database')
        session.close()

    async def delete_user(self, user: User):
        session = self.session_maker()
        session.query(User).filter_by(user_id=user.user_id).delete()
        session.commit()
        await self.logger.warning(f'User {user.user_id} is deleted from database')
        session.close()

    async def get_user_by_id(self, user_id) -> User | None:
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

    async def update_user(self, user: User):
        session = self.session_maker()
        session.query(User).filter_by(user_id=user.user_id).update({
            'user_id': user.user_id,
            'cart': user.cart,
            'order_ids': user.order_ids
        })
        session.commit()
        await self.logger.info(f'User {user.user_id} is updated')
        session.close()

    async def check_product_in_user_cart(self, user_id, product: Product) -> bool:
        session = self.session_maker()
        user = session.query(User).filter_by(user_id=user_id).first()
        if user.cart:
            if product.category in user.cart:
                product_ids = [product_info['product_id'] for product_info in user.cart[product.category]]
                return product.product_id in product_ids
        return False

    async def insert_product_if_not_exist(self, product: Product):
        session = self.session_maker()
        db_product = await self.get_product_by_id(product.product_id)
        if db_product:
            await self.logger.info(f"Product {product.product_id} is already in database")
        else:
            session.add(product)
            session.commit()
            await self.logger.info(f"Product {product.product_id} is added to database")
        session.close()

    async def delete_product(self, product: Product):
        session = self.session_maker()
        session.query(Product).filter_by(product_id=product.product_id).delete()
        session.commit()
        await self.logger.warning(f"Product {product.product_id} is deleted")
        session.close()

    async def get_product_by_id(self, product_id) -> Product | None:
        session = self.session_maker()
        data = session.query(Product).filter(Product.product_id == product_id).first()
        session.close()
        if data:
            await self.logger.info(f"Product {product_id} is retrieved from database")
            return data
        else:
            await self.logger.warning(f"Product {product_id} is not in database")
            return None

    async def get_products_by_category(self, category) -> list | None:
        session = self.session_maker()
        data = session.query(Product).filter(Product.category == category).all()
        session.close()
        if data:
            await self.logger.info(f'Fetched products by category: {category}')
            return data
        else:
            await self.logger.info(f'There are no products with category: {category}')

    async def get_categories(self) -> list | None:
        session = self.session_maker()
        data = session.query(Product).all()
        session.close()
        if data:
            await self.logger.info('Categories is retrieved')
            return sorted(list(set([product.category for product in data])), key=lambda x: x[0])
        else:
            await self.logger.warning('There are no categories')
            return None

    async def update_product(self, product: Product):
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

    async def insert_order(self, order: Order):
        session = self.session_maker()
        session.add(order)
        session.commit()
        await self.logger.info(f'Order {order.order_id} inserted in database')
        session.close()

    async def delete_order(self, order: Order):
        session = self.session_maker()
        session.query(Order).filter_by(order_id=order.order_id).delete()
        session.commit()
        await self.logger.warning(f"Order {order.order_id} is deleted")
        session.close()

    async def get_order_by_id(self, order_id) -> Order | None:
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
