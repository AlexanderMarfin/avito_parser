from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from re import match
from typing import Any
from difflib import SequenceMatcher
from parsers.objects import AUTO_MARKS, AUTO_MODELS

# Ниже реализованы кастомные фильтры хэндлеров.


class ParseLink(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.text[:21] == "https://www.avito.ru/"
            and message.text.find("/avtomobili/") != -1
        )


class FindCity(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        for letter in message.text.lower():
            if not bool(match("[а-яё-]", letter)):
                return False
        return True


class FindRadius(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text in [
            "0",
            "50",
            "75",
            "100",
            "200",
            "300",
            "400",
            "500",
            "1000",
            "2000",
            "3000",
        ]


class FindMark(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.lower() in AUTO_MARKS


class FindMarkByMetric(BaseFilter):
    async def __call__(
        self, message: Message, state: FSMContext
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        if data.get("geo") and (message.text.lower() not in AUTO_MARKS):
            return {
                "mark": AUTO_MARKS[
                    max(
                        enumerate(
                            [
                                SequenceMatcher(None, message.text.lower(), i).ratio()
                                for i in AUTO_MARKS
                            ]
                        ),
                        key=(lambda x: x[1]),
                    )[0]
                ]
            }
        return False


class FindModel(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        data = await state.get_data()
        if data.get("mark"):
            return message.text.lower() in AUTO_MODELS[data.get("mark")]
        return False


class FindModelByMetric(BaseFilter):
    async def __call__(
        self, message: Message, state: FSMContext
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        if data.get("mark") and (
            message.text.lower() not in AUTO_MODELS[data.get("mark")]
        ):
            return {
                "model": AUTO_MODELS[data.get("mark")][
                    max(
                        enumerate(
                            [
                                SequenceMatcher(None, message.text.lower(), i).ratio()
                                for i in AUTO_MODELS[data.get("mark")]
                            ]
                        ),
                        key=(lambda x: x[1]),
                    )[0]
                ]
            }
        return False


class FindPriceFrom(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, Any]:
        if message.text.isdigit() and int(message.text) >= 0:
            return {"price": str(message.text)}
        return False


class FindPriceTo(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        data = await state.get_data()
        if message.text.isdigit() and data.get("price_from") and int(message.text) >= 0:
            if data.get("price_from") != "skip":
                return int(message.text) >= int(data.get("price_from"))
            return True


class FindYearFrom(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, Any]:
        if message.text.isdigit() and 2023 >= int(message.text) >= 1960:
            return {"year": str(message.text)}
        return False


class FindYearTo(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        data = await state.get_data()
        if (
            message.text.isdigit()
            and data.get("year_from")
            and int(message.text) >= 1960
        ):
            if data.get("year_from") != "skip":
                return int(data.get("year_from")) <= int(message.text) <= 2023
            return int(message.text) <= 2023
        return False


class FindMileageFrom(BaseFilter):
    async def __call__(
        self, message: Message, state: FSMContext
    ) -> bool | dict[str, Any]:
        if (
            message.text.isdigit()
            and (int(message.text) % 10000 == 0)
            and int(message.text) >= 0
        ):
            if 500000 >= int(message.text):
                return {"mileage": str(message.text)}
            return {"mileage": "500000+"}
        return False


class FindMileageTo(BaseFilter):
    async def __call__(
        self, message: Message, state: FSMContext
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        if data.get("mileage_from") != "500000+":
            if (
                message.text.isdigit()
                and data.get("mileage_from")
                and (int(message.text) % 10000 == 0)
            ):
                if data.get("mileage_from") != "skip":
                    if 500000 >= int(message.text) >= int(data.get("mileage_from")):
                        return {"mileage": str(message.text)}
                    elif 500000 < int(message.text):
                        return {"mileage": "500000+"}
                else:
                    if 500000 >= int(message.text) >= 0:
                        return {"mileage": str(message.text)}
                    elif 500000 < int(message.text):
                        return {"mileage": "500000+"}
            return False
        return {"mileage": "500000+"}
