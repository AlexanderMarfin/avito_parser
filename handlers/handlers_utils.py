from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import KEYBOARDS
from keyboards import kb_utils
from states.user_states import FSMAutoParsing
from lexicon.lexicon import LEXICON_RU


# Вспомогательные методы для хэндлеров


async def verify_data(data) -> str:
    if data.get("File"):
        data.pop("File")
    keys = [LEXICON_RU[value] for value in data.keys() if value in LEXICON_RU.keys()]
    values = [
        LEXICON_RU[value] if value in LEXICON_RU.keys() else value
        for value in data.values()
    ]
    return "\n".join(x + ": " + y for x, y in zip(keys, values))


async def skip_button(callback: CallbackQuery, state: FSMContext) -> None:
    match await state.get_state():
        case "FSMAutoParsing:mark":
            await state.update_data(mark=callback.data, model=callback.data)
            keyboard = kb_utils.create_inline_kb(
                2, *KEYBOARDS["transmission"], skip="skip"
            )
            await callback.message.answer(
                text=LEXICON_RU["input_transmission"], reply_markup=keyboard
            )
            await state.set_state(FSMAutoParsing.transmission)
        case "FSMAutoParsing:model":
            await state.update_data(model=callback.data)
            keyboard = kb_utils.create_inline_kb(
                2, *KEYBOARDS["transmission"], skip="skip"
            )
            await callback.message.answer(
                text=LEXICON_RU["input_transmission"], reply_markup=keyboard
            )
            await state.set_state(FSMAutoParsing.transmission)
        case "FSMAutoParsing:price_from":
            keyboard = kb_utils.create_inline_kb(1, skip="skip")
            await state.update_data(price_from="skip")
            await callback.message.answer(
                text=LEXICON_RU["input_price_to"] + "0" + ")", reply_markup=keyboard
            )
            await state.set_state(FSMAutoParsing.price_to)
        case "FSMAutoParsing:price_to":
            keyboard = kb_utils.create_inline_kb(1, skip="skip")
            await state.update_data(price_to="skip")
            await callback.message.answer(
                text=LEXICON_RU["input_year_from"], reply_markup=keyboard
            )
            await state.set_state(FSMAutoParsing.year_from)
        case "FSMAutoParsing:year_from":
            keyboard = kb_utils.create_inline_kb(1, skip="skip")
            await state.update_data(year_from="skip")
            await callback.message.answer(
                text=LEXICON_RU["input_year_to"]
                + "1960"
                + LEXICON_RU["input_year_to_1"],
                reply_markup=keyboard,
            )
            await state.set_state(FSMAutoParsing.year_to)
        case "FSMAutoParsing:year_to":
            keyboard = kb_utils.create_inline_kb(1, skip="skip")
            await state.update_data(year_to="skip")
            await callback.message.answer(
                text=LEXICON_RU["input_mileage_from"], reply_markup=keyboard
            )
            await state.set_state(FSMAutoParsing.mileage_from)
        case "FSMAutoParsing:mileage_from":
            keyboard = kb_utils.create_inline_kb(1, skip="skip")
            await state.update_data(mileage_from="skip")
            await callback.message.answer(
                text=LEXICON_RU["input_mileage_to"]
                + "0"
                + LEXICON_RU["input_mileage_to_1"],
                reply_markup=keyboard,
            )
            await state.set_state(FSMAutoParsing.mileage_to)
        case "FSMAutoParsing:mileage_to":
            keyboard = kb_utils.create_inline_kb(
                1, *KEYBOARDS["start_parse"], skip=None
            )
            await state.update_data(mileage_to="skip")
            await callback.message.answer(
                text=LEXICON_RU["check_data"]
                + f"\n\n{await verify_data(await state.get_data())}",
                reply_markup=keyboard,
            )
            await state.set_state(FSMAutoParsing.start_parsing)
