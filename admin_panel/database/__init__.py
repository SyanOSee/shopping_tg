from .db import Database, Type
from admin_panel.logger import Logger
import admin_panel.config as cf

database = Database(type_=Type.POSTGRESQL, logger=Logger(cf.project['log']))