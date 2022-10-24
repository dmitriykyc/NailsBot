from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Записаться')
        ],
        [
            KeyboardButton(text='Личный кабинет')
        ],
        [
            KeyboardButton(text='О нас')
        ],
        [
            KeyboardButton(text='🤩Как сделать такого бота себе?🤩')
        ],
[
            KeyboardButton(text='🤔Что ещё умеет этот бот?🤔')
        ]
    ], resize_keyboard=True
)
