from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import StateFilter, or_f
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from parsers.auto_parser import AutoParser
from parsers.parser_utils import get_url, get_statistics, get_plot
from handlers.handlers_utils import skip_button, verify_data
from lexicon.lexicon import LEXICON_RU
from keyboards import kb_utils
from keyboards.keyboards import KEYBOARDS
from states.user_states import FSMAutoParsing
from filters.filters import (
    FindCity,
    FindRadius,
    FindMark,
    FindModel,
    FindPriceFrom,
    FindPriceTo,
    FindYearFrom,
    FindYearTo,
    FindMileageFrom,
    FindMileageTo,
    FindMarkByMetric,
    FindModelByMetric,
)


# Инициализируем роутер уровня модуля
router = Router()

# Хэндлеры поиска и выгрузки объявлений авто


@router.message(
    F.text == LEXICON_RU["auto_finder"], StateFilter(FSMAutoParsing.choose)
)
async def process_find(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=LEXICON_RU["input_city"], reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FSMAutoParsing.city)


@router.message(
    FindCity(), StateFilter(FSMAutoParsing.city)
)
async def find_city(message: Message, state: FSMContext) -> None:
    await state.update_data(geo=message.text.lower())
    await message.answer(
        text=LEXICON_RU["input_radius"], reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FSMAutoParsing.radius)


@router.message(
    ~FindCity(), StateFilter(FSMAutoParsing.city)
)
async def find_city_invert(message: Message, state: FSMContext) -> None:
    await message.answer(text=LEXICON_RU["input_wrong_city"])
    await state.set_state(FSMAutoParsing.city)


@router.message(
    ~FindRadius(), StateFilter(FSMAutoParsing.radius)
)
async def find_radius_invert(message: Message, state: FSMContext) -> None:
    await message.answer(text=LEXICON_RU["input_wrong_radius"])
    await state.set_state(FSMAutoParsing.radius)


@router.message(
    FindRadius(), StateFilter(FSMAutoParsing.radius)
)
async def find_radius(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await state.update_data(radius=message.text)
    await message.answer(text=LEXICON_RU["input_mark"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.mark)


@router.message(
    FindMark(), StateFilter(FSMAutoParsing.mark)
)
async def find_mark(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await state.update_data(mark=message.text.lower())
    await message.answer(text=LEXICON_RU["input_model"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.model)


@router.message(
    FindMarkByMetric(), StateFilter(FSMAutoParsing.mark)
)
async def find_mark_invert(message: Message, state: FSMContext, mark: str) -> None:
    await message.answer(text=LEXICON_RU["input_wrong_name"] + mark + "?")
    await state.set_state(FSMAutoParsing.mark)


@router.message(
    FindModel(), StateFilter(FSMAutoParsing.model)
)
async def find_model(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(2, *KEYBOARDS["transmission"], skip="skip")
    await state.update_data(model=message.text.lower())
    await message.answer(text=LEXICON_RU["input_transmission"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.transmission)


@router.message(
    FindModelByMetric(), StateFilter(FSMAutoParsing.model)
)
async def find_model_invert(message: Message, state: FSMContext, model: str) -> None:
    await message.answer(text=LEXICON_RU["input_wrong_name"] + model + "?")
    await state.set_state(FSMAutoParsing.model)


@router.callback_query(
    or_f(F.data.in_(KEYBOARDS["transmission"]), F.data == "skip"),
    StateFilter(FSMAutoParsing.transmission),
)
async def find_transmission(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(transmission=callback.data)
    keyboard = kb_utils.create_inline_kb(2, *KEYBOARDS["engine"], skip="skip")
    await callback.message.answer(
        text=LEXICON_RU["input_engine"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.engine)


@router.callback_query(
    ~or_f(F.data.in_(KEYBOARDS["transmission"]), F.data == "skip"),
    StateFilter(FSMAutoParsing.transmission),
)
async def find_transmission_invert(callback: CallbackQuery, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(2, *KEYBOARDS["transmission"], skip="skip")
    await callback.message.answer(
        text=LEXICON_RU["input_wrong_transmission"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.transmission)


@router.callback_query(
    or_f(F.data.in_(KEYBOARDS["engine"]), F.data == "skip"),
    StateFilter(FSMAutoParsing.engine),
)
async def find_engine(callback: CallbackQuery, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(3, *KEYBOARDS["gear"], skip="skip")
    await state.update_data(engine=callback.data)
    await callback.message.answer(text=LEXICON_RU["input_gear"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.gear)


@router.callback_query(
    ~or_f(F.data.in_(KEYBOARDS["engine"]), F.data == "skip"),
    StateFilter(FSMAutoParsing.engine),
)
async def find_engine_invert(callback: CallbackQuery, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(2, *KEYBOARDS["engine"], skip="skip")
    await callback.message.answer(
        text=LEXICON_RU["input_wrong_engine"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.engine)


@router.callback_query(
    or_f(F.data.in_(KEYBOARDS["gear"]), F.data == "skip"),
    StateFilter(FSMAutoParsing.gear),
)
async def find_gear(callback: CallbackQuery, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await state.update_data(gear=callback.data)
    await callback.message.answer(
        text=LEXICON_RU["input_price_from"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.price_from)


@router.callback_query(
    or_f(~F.data.in_(KEYBOARDS["gear"]), F.data == "skip"),
    StateFilter(FSMAutoParsing.gear),
)
async def find_gear_invert(callback: CallbackQuery, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(3, *KEYBOARDS["gear"], skip="skip")
    await callback.message.answer(
        text=LEXICON_RU["input_wrong_gear"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.gear)


@router.message(
    FindPriceFrom(), StateFilter(FSMAutoParsing.price_from)
)
async def find_price_from(message: Message, state: FSMContext, price: str) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await state.update_data(price_from=message.text)
    await message.answer(
        text=LEXICON_RU["input_price_to"] + price + ")", reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.price_to)


@router.message(
    ~FindPriceFrom(), StateFilter(FSMAutoParsing.price_from)
)
async def find_price_from_invert(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await message.answer(
        text=LEXICON_RU["input_wrong_price_from"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.price_from)


@router.message(
    FindPriceTo(), StateFilter(FSMAutoParsing.price_to)
)
async def find_price_to(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await state.update_data(price_to=message.text)
    await message.answer(text=LEXICON_RU["input_year_from"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.year_from)


@router.message(
    ~FindPriceTo(), StateFilter(FSMAutoParsing.price_to)
)
async def find_price_to_invert(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await message.answer(text=LEXICON_RU["input_wrong_price_to"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.price_to)


@router.message(
    FindYearFrom(), StateFilter(FSMAutoParsing.year_from)
)
async def find_year_from(message: Message, state: FSMContext, year: str) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await state.update_data(year_from=message.text)
    await message.answer(
        text=LEXICON_RU["input_year_to"] + year + LEXICON_RU["input_year_to_1"],
        reply_markup=keyboard,
    )
    await state.set_state(FSMAutoParsing.year_to)


@router.message(
    ~FindYearFrom(), StateFilter(FSMAutoParsing.year_from)
)
async def find_year_from_invert(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await message.answer(
        text=LEXICON_RU["input_wrong_year_from"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.year_from)


@router.message(
    FindYearTo(), StateFilter(FSMAutoParsing.year_to)
)
async def find_year_to(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await state.update_data(year_to=message.text)
    await message.answer(text=LEXICON_RU["input_mileage_from"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.mileage_from)


@router.message(
    ~FindYearTo(), StateFilter(FSMAutoParsing.year_to)
)
async def find_year_to_invert(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await message.answer(text=LEXICON_RU["input_wrong_year_to"], reply_markup=keyboard)
    await state.set_state(FSMAutoParsing.year_to)


@router.message(
    FindMileageFrom(), StateFilter(FSMAutoParsing.mileage_from)
)
async def find_mileage_from(message: Message, state: FSMContext, mileage: str) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await state.update_data(mileage_from=mileage)
    if mileage != "500000+":
        await message.answer(
            text=LEXICON_RU["input_mileage_to"]
            + mileage
            + LEXICON_RU["input_mileage_to_1"],
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=LEXICON_RU["input_mileage_to_2"], reply_markup=keyboard
        )
    await state.set_state(FSMAutoParsing.mileage_to)


@router.message(
    ~FindMileageFrom(), StateFilter(FSMAutoParsing.mileage_from)
)
async def find_mileage_from_invert(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await message.answer(
        text=LEXICON_RU["input_wrong_mileage_from"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.mileage_from)


@router.message(
    FindMileageTo(), StateFilter(FSMAutoParsing.mileage_to)
)
async def start_parsing(message: Message, state: FSMContext, mileage: str) -> None:
    await state.update_data(mileage_to=mileage)
    keyboard = kb_utils.create_inline_kb(1, *KEYBOARDS["start_parse"], skip=None)
    await message.answer(
        text=LEXICON_RU["check_data"]
        + f"\n\n{await verify_data(await state.get_data())}",
        reply_markup=keyboard,
    )
    await state.set_state(FSMAutoParsing.start_parsing)


@router.callback_query(
    F.data == "start_parsing",
    StateFilter(FSMAutoParsing.start_parsing),
    flags={"parser": "parser"},
)
async def find_mileage_to(
    callback: CallbackQuery, state: FSMContext, parser: AutoParser
) -> None:
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    bot_message = await callback.message.answer(text=LEXICON_RU["generate"])
    data = await state.get_data()
    await state.set_state(FSMAutoParsing.choose)
    if await parser.url_master(data):
        await parser.set_transmission(data.get("transmission"))
        await parser.set_engine(data.get("engine"))
        await parser.set_gear(data.get("gear"))
        await parser.set_price(data.get("price_from"), 2)
        await parser.set_price(data.get("price_to"), 3)
        await parser.set_year_mileage(data.get("year_from"), 0)
        await parser.set_year_mileage(data.get("year_to"), 1)
        await parser.set_year_mileage(data.get("mileage_from"), 2)
        await parser.set_year_mileage(data.get("mileage_to"), 3)
        await get_url(callback.message, state, parser, bot_message)
    else:
        await callback.message.answer(
            text=LEXICON_RU["not_found"] + LEXICON_RU["check_input"],
            reply_markup=keyboard,
        )


@router.callback_query(
    F.data.in_(KEYBOARDS["statistics"]), StateFilter(FSMAutoParsing.statistics)
)
async def statistics(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    match callback.data:
        case "menu":
            await callback.message.answer(
                text=LEXICON_RU["do_next"],
                reply_markup=kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"]),
            )
            await state.set_state(FSMAutoParsing.choose)
        case "info":
            keyboard = kb_utils.create_inline_kb(2, *KEYBOARDS["statistics"], skip=None)
            await callback.message.answer_photo(
                photo=await get_statistics(
                    data.get("file"), callback.message.from_user.id
                ),
                reply_markup=keyboard,
            )
            await state.set_state(FSMAutoParsing.statistics)
        case "plot":
            keyboard = kb_utils.create_inline_kb(2, *KEYBOARDS["statistics"], skip=None)
            await callback.message.answer_photo(
                photo=await get_plot(
                    data.get("file"), callback.message.from_user.id
                ),
                reply_markup=keyboard,
            )
            await state.set_state(FSMAutoParsing.statistics)


@router.callback_query(
    F.data == "retry",
    StateFilter(FSMAutoParsing.statistics),
    flags={"parser": "parser"},
)
async def process_retry_parsing(
    callback: CallbackQuery, state: FSMContext, parser: AutoParser
) -> None:
    await callback.message.answer(text=LEXICON_RU["generate"])
    await state.set_state(FSMAutoParsing.choose)
    await get_url(callback.message, state, parser)


@router.message(
    ~FindMileageTo(), StateFilter(FSMAutoParsing.mileage_to)
)
async def find_mileage_to_invert(message: Message, state: FSMContext) -> None:
    keyboard = kb_utils.create_inline_kb(1, skip="skip")
    await message.answer(
        text=LEXICON_RU["input_wrong_mileage_to"], reply_markup=keyboard
    )
    await state.set_state(FSMAutoParsing.mileage_to)


@router.callback_query(
    F.data == "reset_data", StateFilter(FSMAutoParsing.start_parsing)
)
async def reset_data(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer(
        text=LEXICON_RU["input_city"], reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FSMAutoParsing.city)


@router.callback_query(
    F.data == "skip"
)
async def skip(callback: CallbackQuery, state: FSMContext) -> None:
    await skip_button(callback, state)
