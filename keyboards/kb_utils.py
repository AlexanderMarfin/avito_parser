from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


# Функция для генерации инлайн-клавиатуры
def create_inline_kb(
    width: int, *args: str, skip: str | None, **kwargs: str
) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    for button in args:
        buttons.append(
            InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button,
            )
        )
    for button, text in kwargs.items():
        buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if skip:
        kb_builder.row(
            InlineKeyboardButton(
                text=LEXICON_RU[skip] if skip in LEXICON_RU else skip,
                callback_data=skip,
            )
        )

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Функция для генерации reply-клавиатуры на лету
def create_reply_kb(
    width: int, *args: str, one_time_keyboard: bool = True
) -> ReplyKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[KeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(
                KeyboardButton(
                    text=LEXICON_RU[button] if button in LEXICON_RU else button
                )
            )

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(
        resize_keyboard=True, one_time_keyboard=one_time_keyboard
    )
