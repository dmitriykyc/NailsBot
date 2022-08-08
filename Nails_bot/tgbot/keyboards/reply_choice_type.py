from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_choice_type = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выбрать мастера'),
            KeyboardButton(text='Выбрать услугу')
        ]
    ], resize_keyboard=True
)