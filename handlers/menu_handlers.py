from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_RU
from keyboards import kb_utils
from states.user_states import FSMAutoParsing
from parsers.auto_parser import AutoParser
from parsers.parser_utils import start_parse
from keyboards.keyboards import KEYBOARDS
from filters.filters import ParseLink


# Инициализируем роутер уровня модуля
router = Router()


# Хэндлеры меню


@router.message(
    F.text == LEXICON_RU["unloading"], StateFilter(FSMAutoParsing.choose)
)
async def process_choose(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["unloading_menu"])
    await message.answer(text=LEXICON_RU["unloading_choose"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.choose_parsing)


@router.message(
    F.text == LEXICON_RU["auto_parse"], StateFilter(FSMAutoParsing.choose_parsing)
)
async def process_auto_parse(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=LEXICON_RU["unloading_auto"], reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FSMAutoParsing.auto_parse)


@router.message(
    ParseLink(), StateFilter(FSMAutoParsing.auto_parse), flags={"parser": "parser"}
)
async def process_auto_parsing(message: Message, state: FSMContext, parser: AutoParser) -> None:
    await state.set_state(FSMAutoParsing.choose)
    await start_parse(message, message.text, parser, state)


@router.message(
    ~ParseLink(), StateFilter(FSMAutoParsing.auto_parse)
)
async def process_auto_parsing(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMAutoParsing.auto_parse)
    await message.answer(
        text=LEXICON_RU["wrong_auto_link"], reply_markup=ReplyKeyboardRemove()
    )


@router.message(
    F.text == LEXICON_RU["flat_parse"], StateFilter(FSMAutoParsing.choose_parsing)
)
async def process_flat_parse(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await message.answer(text=LEXICON_RU["in_progress"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.choose)


@router.message(
    F.text == LEXICON_RU["back"], StateFilter(FSMAutoParsing.choose_parsing)
)
async def process_flat_parse(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await message.answer(text=LEXICON_RU["/start"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.choose)
