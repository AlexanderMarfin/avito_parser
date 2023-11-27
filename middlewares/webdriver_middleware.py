from typing import Any, Awaitable, Callable, Dict, Union
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.flags import get_flag
from parsers.auto_parser import AutoParser
from aiogram.fsm.storage.redis import RedisStorage
from selenium.common.exceptions import InvalidSessionIdException

# Инициализация экземляра парсера


class WebdriverMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage) -> None:
        self.storage = storage
        self.parser = None

    async def __call__(
        self,
        handler: Callable[
            [Union[CallbackQuery, Message], Dict[str, Any]], Awaitable[Any]
        ],
        event: Union[CallbackQuery, Message],
        data: Dict[str, Any],
    ) -> Any:
        # Если флага на хэндлере нет
        if not get_flag(data, "parser"):
            return await handler(event, data)
        if self.parser:
            try:
                await self.parser.quit_webdriver()
            except InvalidSessionIdException:
                pass
        self.parser = AutoParser()
        data['parser'] = self.parser
        return await handler(event, data)
