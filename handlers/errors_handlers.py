import logging
from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Message, CallbackQuery, ErrorEvent
from lexicon.lexicon import LEXICON_RU
from keyboards import kb_utils
from keyboards.keyboards import KEYBOARDS
from selenium.common.exceptions import WebDriverException, TimeoutException
from aiogram.fsm.context import FSMContext
from states.user_states import FSMAutoParsing


# Инициализируем роутер уровня модуля
router = Router()

# Хэндлеры ошибок


@router.error(ExceptionTypeFilter(TimeoutException), F.update.message.as_("message"))
async def timeout_handler_message(
    event: ErrorEvent, message: Message, state: FSMContext
) -> None:
    await state.set_state(FSMAutoParsing.choose)
    logging.critical("Webdriver timeout!")
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await message.answer(text=LEXICON_RU["timeout_error"], reply_markup=keyboard)


@router.error(
    ExceptionTypeFilter(TimeoutException), F.update.message.as_("callback_query")
)
async def timeout_handler_callback(
    event: ErrorEvent, callback_query: CallbackQuery, state: FSMContext
) -> None:
    logging.critical("Webdriver timeout!")
    keyboard = kb_utils.create_inline_kb(1, *KEYBOARDS["error_menu"], skip=None)
    await callback_query.message.answer(
        text=LEXICON_RU["timeout_error"], reply_markup=keyboard
    )


@router.error(ExceptionTypeFilter(WebDriverException), F.update.message.as_("message"))
async def webdriver_error_message_handler(
    event: ErrorEvent, message: Message, state: FSMContext
) -> None:
    await state.set_state(FSMAutoParsing.choose)
    logging.critical("Webdriver exception!")
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await message.answer(text=LEXICON_RU["parse_error"], reply_markup=keyboard)


@router.error(
    ExceptionTypeFilter(WebDriverException), F.update.message.as_("callback_query")
)
async def webdriver_error_callback_handler(
    event: ErrorEvent, callback_query: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(FSMAutoParsing.choose)
    logging.critical("Webdriver exception!")
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await callback_query.message.answer(
        text=LEXICON_RU["parse_error"], reply_markup=keyboard
    )


@router.error(F.update.message.as_("message"))
async def unhandled_error_handler(
    event: ErrorEvent, message: Message, state: FSMContext
) -> None:
    await state.set_state(FSMAutoParsing.choose)
    logging.critical("Unhandled error: %s", event.exception, exc_info=True)
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await message.answer(text=LEXICON_RU["something_wrong"], reply_markup=keyboard)
