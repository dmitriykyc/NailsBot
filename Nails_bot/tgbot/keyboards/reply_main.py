from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Записаться')
        ],
        [
            KeyboardButton(text='О нас'),
            KeyboardButton(text='Виды услуг и цены')
        ]
    ], resize_keyboard=True
)
