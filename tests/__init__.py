from unittest import IsolatedAsyncioTestCase as AsyncioTest
import os

async def start_all_tests():
    os.system("python -m unittest discover tests")


if __name__ == '__main__':
    import asyncio

    asyncio.new_event_loop().run_until_complete(start_all_tests())
