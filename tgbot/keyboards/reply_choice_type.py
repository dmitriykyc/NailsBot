from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_master_or_serv():
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[[
                                    InlineKeyboardButton(text='Выбрать мастера', callback_data='choose_master_main')
                                ],
                                    [
                                        InlineKeyboardButton(text='Выбрать услугу', callback_data='choose_service_main')
                                    ]])

    return menu
