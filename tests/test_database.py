from unittest import IsolatedAsyncioTestCase as AsyncioTest
from init_loader import db
from data.database.models import User, Product, Order


class test_database(AsyncioTest):
    async def test_insert_user_if_not_exist(self):
        user = User().init_values(139)
        await db.insert_user_if_not_exist(user)
        self.assertTrue(await db.get_user_by_id(user.user_id) is not None)
        await db.delete_user(user)

    async def test_get_user_by_id(self):
        user = User().init_values(123)
        await db.insert_user_if_not_exist(user)
        retrieved_user = await db.get_user_by_id(user.user_id)
        none = await db.get_user_by_id(-1919191919)
        self.assertTrue(retrieved_user is not None and none is None)
        await db.delete_user(user)

    async def test_update_user(self):
        user = User().init_values(12313)
        await db.insert_user_if_not_exist(user)
        updated_user = User().init_values(12313, {'1': 1}, [1, 2])
        await db.update_user(updated_user)
        retrieved_user = await db.get_user_by_id(updated_user.user_id)
        self.assertTrue(retrieved_user.cart == updated_user.cart)
        self.assertTrue(retrieved_user.order_ids == updated_user.order_ids)
        await db.delete_user(user)

    async def test_delete_user(self):
        user = User().init_values(9090)
        await db.insert_user_if_not_exist(user)
        await db.delete_user(user)
        self.assertTrue(await db.get_user_by_id(user.user_id) is None)

    async def test_insert_product_if_not_exist(self):
        product = Product().init_values(1424, 'cat1', 'drum', 'super cool drum', 'C://drum.png', 12000, 12, 5)
        await db.insert_product_if_not_exist(product)
        self.assertTrue(await db.get_product_by_id(product.product_id) is not None)
        await db.delete_product(product)

    async def test_get_product_by_id(self):
        product = Product().init_values(845, 'cat2', 'js', 'super cool js', 'C://js.png', 1, 32)
        await db.insert_product_if_not_exist(product)
        retrieved_product = await db.get_product_by_id(product.product_id)
        none = await db.get_product_by_id(-1919191919)
        self.assertTrue(retrieved_product is not None and none is None)
        await db.delete_product(product)

    async def test_get_products_by_category(self):
        category = 'category'
        product = Product().init_values(845, category, 'js', 'super cool js', 'C://js.png', 1, 32)
        await db.insert_product_if_not_exist(product)
        products = await db.get_products_by_category(category)
        self.assertTrue(products[0] is not None)
        self.assertTrue(await db.get_products_by_category('test') is None)
        await db.delete_product(product)

    async def get_categories(self):
        categories = ['category', 'category1']
        product = Product().init_values(845, categories[0], 'js', 'super cool js', 'C://js.png', 1, 32)
        product1 = Product().init_values(845, categories[1], 'js', 'super cool js', 'C://js.png', 1, 32)
        await db.insert_product_if_not_exist(product)
        self.assertTrue(await db.get_categories() == categories)
        await db.delete_product(product)
        await db.delete_product(product1)
        self.assertTrue(await db.get_categories() is None)

    async def test_update_product(self):
        product = Product().init_values(9090, 'cat68', '12', 'asd cool drum', 'C://dj.png', 12000, 12, 5)
        await db.insert_product_if_not_exist(product)
        updated_product = await db.get_product_by_id(product.product_id)
        updated_product.category = 'super duper category'
        await db.update_product(updated_product)
        retrieved_product = await db.get_product_by_id(updated_product.product_id)
        self.assertTrue(retrieved_product.category == updated_product.category)
        await db.delete_product(updated_product)

    async def test_delete_product(self):
        product = Product().init_values(8383, 'cat68', '12', 'asd cool drum', 'C://dj.png', 12000, 12, 5)
        await db.insert_product_if_not_exist(product)
        await db.delete_product(product)
        self.assertTrue(await db.get_product_by_id(product.product_id) is None)

    async def test_insert_order(self):
        import datetime

        order = Order().init_values('123515', {
            'products': [
                {
                    'name': 'some',
                    'amount': 12
                }, {
                    'name': 'any',
                    'amount': 15
                }
            ]
        }, 'midirovo 12/141c', datetime.datetime(day=12, month=12, year=12))

        await db.insert_order(order)
        self.assertTrue(await db.get_order_by_id(order.order_id) is not None)
        await db.delete_order(order)
