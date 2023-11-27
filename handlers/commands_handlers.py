from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram import Router, F, flags
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_RU
from keyboards import kb_utils
from states.user_states import FSMAutoParsing
from database.methods.create import create_user
from asyncio import sleep
from keyboards.keyboards import KEYBOARDS

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext) -> None:
    create_user(message.from_user.id, message.from_user.username)
    await sleep(1)
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await message.answer(text=LEXICON_RU["/start"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.choose)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands="help"))
async def process_help_command(message: Message) -> None:
    await sleep(1)
    await message.answer(text=LEXICON_RU["/help"])


# Этот хэндлер срабатывает на команду /reset
@router.message(Command(commands="reset"), ~StateFilter(default_state))
async def process_reset_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await message.answer(text=LEXICON_RU["/reset"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.choose)
