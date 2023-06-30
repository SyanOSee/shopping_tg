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