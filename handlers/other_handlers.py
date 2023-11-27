from aiogram.types import Message
from aiogram import Router
from lexicon.lexicon import LEXICON_RU

# Инициализируем роутер уровня модуля
router = Router()

# Хэндлер неизвестных апдейтов


@router.message()
async def send_echo(message: Message) -> None:
    await message.reply(text=LEXICON_RU["unknown"])
