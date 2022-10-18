from sqlalchemy import *

from utils.logger import Logger

EXAMPLE_TABLE = "ExampleTable"


class Database:
    def __init__(self, info, logger: Logger):  # info is named tuple
        self.__engine = create_engine(
            # f"postgresql://{info.user}:{info.password}@{info.host}:{info.port}" Postgresql
            # f"sqlite:///{info.path}" Sqlite
        )
        self.__conn = self.__engine.connect()

        self.__logger = logger

        self.__metadata = MetaData()

        self.example_table = Table(EXAMPLE_TABLE, self.__metadata,
                                         Column("id", Integer(), primary_key=True, autoincrement=True),
                                         Column("arg1", String(), nullable=False),
                                         Column("arg2", Text(), default=""),
                                         )

        self.__metadata.create_all(self.__engine)

    async def insert_example(self, model: Model):
        insertion = self.example_table.insert().values(
            arg1=model.arg1,
            arg2=model.arg2
        )

        await self.__logger.info("DATABASE INSERTION EXAMPLE")
        self.__conn.execute(insertion)

    async def delete_example(self, model: Model):
        deletion = self.example_table.delete().where(
            self.example_table.columns.arg1 == model.arg1
        )

        self.__logger.info("DATABASE DELETION EXAMPLE")
        self.__conn.execute(deletion)

    async def select_example(self, arg1) -> Model | None:
        selection = self.example_table.select().where(
            self.example_table.columns.arg1 == arg1
        )

        data = self.__conn.execute(selection).fetchone()
        await self.__logger.info("DATABASE SELECTION EXAMPLE")
        if data is not None:
            arg1, arg2 = data
            return Model(arg1, arg2)
        else:
            return None

    async def update_example(self, model: Model):
        update = self.example_table.update().where(
            self.example_table.columns.arg1 == model.arg1
        ).values(
            arg2=model.arg2
        )

        await self.__logger.info("DATABASE UPDATE EXAMPLE")
        self.__conn.execute(update)
