from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, TelegramObject

# Троттлинг


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_message = f"um{event.from_user.id}"

        check_user = await self.storage.redis.get(name=user_message)

        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user_message, value=1, ex=3)
                return await event.answer(
                    "Не нужно писать так часто! Подождите 3 секунды."
                )
            return
        await self.storage.redis.set(name=user_message, value=1, px=500)

        return await handler(event, data)
