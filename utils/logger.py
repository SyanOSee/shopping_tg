import logging as log

class Logger:
    def __init__(self, logging_path: str = ""):
        self.__logging_path = logging_path
        log.basicConfig(  # formatting output string
            format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            filename=logging_path,
            level=log.INFO
        )

    @staticmethod
    async def __show_in_console(msg: str):
        print(msg)

    async def get_logging_path(self) -> str:
        return self.__logging_path

    async def read_log_file(self) -> str:
        if self.__logging_path:
            with open(self.__logging_path, "r") as f:
                return f.read()
        return ""

    async def clear_log_file(self):
        if self.__logging_path:
            with open(self.__logging_path, "w") as f:
                f.write("")
        return ""

    @staticmethod
    async def info(msg: str):
        await Logger.__show_in_console(msg)
        log.info(msg=msg)

    @staticmethod
    async def warning(msg: str):
        await Logger.__show_in_console(msg)
        log.warning(msg=msg)

    @staticmethod
    async def error(msg: str):
        await Logger.__show_in_console(msg)
        log.error(msg=msg)
