# Third-party
import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

# Standard
from typing import Callable, Dict, Any, Awaitable

# Project
from modules import logger


def clear_dict(dict_: dict) -> dict:
    cleared_dict = {}
    for key, value in dict_.items():
        if dict_[key]:
            if key not in cleared_dict:
                cleared_dict[key] = ''
            cleared_dict[key] = value
    return cleared_dict


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        logger.info('Handling event:\n' + str(clear_dict(event.model_dump())))
        result = await handler(event, data)
        return result
