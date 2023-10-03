# Third-party
from sqlalchemy import *
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker

# Standard
from time import sleep
from enum import Enum
import traceback

# Project
from admin_panel import config as cf
from admin_panel.logger import Logger
from admin_panel.database.models import base


# Enum for different types of database connections
class Type(Enum):
    POSTGRESQL = f'postgresql://{cf.database["user"]}:{cf.database["password"]}@{cf.database["host"]}:{cf.database["port"]}'


# Class for managing database connections and operations
class Database:
    # Private method to connect to the database
    def __connect_to_database(self, type_: Type):
        while True:
            self.logger.warning('Connecting to database...')
            try:
                # Creating a database engine
                self.engine = create_engine(type_.value)
                self.session_maker = sessionmaker(bind=self.engine)
                # Creating tables defined in 'base' metadata
                base.metadata.create_all(self.engine)
                self.logger.info('Connected to database')
                break
            except sqlalchemy.exc.OperationalError:
                # Handling database connection errors
                self.logger.error('Database error:\n' + traceback.format_exc())
                sleep(5.0)

    # Constructor to initialize the Database class
    def __init__(self, type_: Type, logger: Logger):
        self.logger = logger
        self.__connect_to_database(type_=type_)
