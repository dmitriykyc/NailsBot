from aiogram.dispatcher.filters.state import StatesGroup, State


class CheckName(StatesGroup):
    Q1 = State()  # Начальная стадия проверки имени
    Q2 = State()  # Изменение имени
    Q3 = State()  # Подтверждённое или изменённое имя и финал
