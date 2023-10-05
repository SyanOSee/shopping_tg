from .db import Database, Type
from logger import Logger
import config as cf

database = Database(type_=Type.POSTGRESQL, logger=Logger(cf.project['log']))