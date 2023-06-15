from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from data.database.models import Models

class Database:
    def __init__(self, info, logger):
        self.engine = create_engine(
            f'sqlite:///{info.path}?check_same_thread=False')  # Use the provided connection string directly
        self.session_maker = sessionmaker(bind=self.engine)
        self.logger = logger

        Models.base.metadata.create_all(self.engine)

    async def insert_user_if_not_exist(self, user: Models.User):
        session = self.session_maker()
        db_user = await self.get_user_by_id(user.user_id)
        if db_user:
            await self.logger.info(f'User {user.user_id} is already in database')
        else:
            session.add(user)
            session.commit()
            await self.logger.info(f'User {user.user_id} is added to database')
        session.close()

    async def delete_user(self, user: Models.User):
        session = self.session_maker()
        session.query(Models.User).filter_by(user_id=user.user_id).delete()
        session.commit()
        await self.logger.warning(f'User {user.user_id} is deleted from database')
        session.close()

    async def get_user_by_id(self, user_id) -> Models.User | None:
        session = self.session_maker()
        data = session.query(Models.User).filter(Models.User.user_id == user_id).first()
        if data:
            await self.logger.info(f'User {user_id} is retrieved from database')
            session.close()
            return data
        else:
            await self.logger.warning(f'User {user_id} is not in database')
            session.close()
            return None

    async def update_user(self, user: Models.User):
        session = self.session_maker()
        db_user = session.query(Models.User).filter_by(user_id=user.user_id).first()
        db_user.basket = user.basket
        db_user.order_ids = user.order_ids
        session.commit()
        await self.logger.info(f'User {user.user_id} is updated')
        session.close()

    async def insert_product_if_not_exist(self, product: Models.Product):
        session = self.session_maker()
        db_product = await self.get_product_by_id(product.product_id)
        if db_product:
            await self.logger.info(f"Product {product.product_id} is already in database")
        else:
            session.add(product)
            session.commit()
            await self.logger.info(f"Product {product.product_id} is added to database")
        session.close()

    async def delete_product(self, product: Models.Product):
        session = self.session_maker()
        session.query(Models.Product).filter_by(product_id=product.product_id).delete()
        session.commit()
        await self.logger.warning(f"Product {product.product_id} is deleted")
        session.close()

    async def get_product_by_id(self, product_id) -> Models.Product | None:
        session = self.session_maker()
        data = session.query(Models.Product).filter(Models.Product.product_id == product_id).first()
        session.close()
        if data:
            await self.logger.info(f"Product {product_id} is retrieved from database")
            return data
        else:
            await self.logger.warning(f"Product {product_id} is not in database")
            return None

    async def update_product(self, product: Models.Product):
        session = self.session_maker()
        db_product = session.query(Models.Product).filter_by(product_id=product.product_id).first()
        db_product.category = product.category
        db_product.name = product.name
        db_product.description = product.description
        db_product.image_url = product.image_url
        db_product.cost = product.cost
        db_product.amount = product.amount
        db_product.discount = product.discount
        session.commit()
        await self.logger.info(f'Product {product.product_id} is updated')
        session.close()

    async def insert_order(self, order: Models.Order):
        session = self.session_maker()
        session.add(order)
        session.commit()
        await self.logger.info(f'Order {order.order_id} inserted in database')
        session.close()

    async def delete_order(self, order: Models.Order):
        session = self.session_maker()
        session.query(Models.Order).filter_by(order_id=order.order_id).delete()
        session.commit()
        await self.logger.warning(f"Order {order.order_id} is deleted")
        session.close()

    async def get_order_by_id(self, order_id) -> Models.Order | None:
        session = self.session_maker()
        data = session.query(Models.Order).filter_by(order_id=order_id).first()
        if data:
            await self.logger.info(f'Order {order_id} is retrieved from database')
            session.close()
            return data
        else:
            await self.logger.warning(f'Order {order_id} not in database')
            session.close()
            return None
