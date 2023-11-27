from typing import Iterator
from aiogram.filters.state import State, StatesGroup


# Класс, для группы состояний  FSM
class FSMAutoParsing(StatesGroup):
    # Экземпляры класса State
    # Возможные состояния, в которых будет находиться бот в разные моменты взаимодействия с пользователем
    choose = State()  # Состояние выбора действия
    city = State()  # Состояние ввода города поиска
    radius = State()  # Состояние ввода радиуса поиска
    mark = State()  # Состояние ввода марки авто
    model = State()  # Состояние ввода модели авто
    transmission = State()  # Состояние выбора трансмиссии
    engine = State()  # Состояние выбора двигателя
    gear = State()  # ССостояние выбора привода
    price_from = State()  # Состояние ввода цены от
    price_to = State()  # Состояние ввода цены до
    year_from = State()  # Состояние ввода года от
    year_to = State()  # Состояние ввода года до
    mileage_from = State()  # Состояние ввода пробега от
    mileage_to = State()  # Состояние ввода пробега до
    start_parsing = State()  # Состояние начала парсинга
    choose_parsing = State()  # Состояние выбора парсинга
    auto_parse = State()  # Состояние выбора парсинга авто
    flat_parse = State()  # Состояние выбора парсинга квартир
    statistics = State()  # Состояние вывода статистики

    # Метод для получения предыдущего состояния из списка
    # состояний стейтгруппы
    @classmethod
    def get_previous_state(cls, state: State) -> State:
        states: Iterator[State] = iter(cls)
        result: State = next(states)

        for state_ in states:
            if state_ == state:
                break
            result = state_

        return result
