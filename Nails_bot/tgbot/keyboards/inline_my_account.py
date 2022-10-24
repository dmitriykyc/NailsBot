from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_my_account_data import my_account_data


def get_my_account_menu(id_appointment):
    menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[
        InlineKeyboardButton(text='⛔ Отменить', callback_data=my_account_data.new(
            id_appointment=id_appointment
        ))
    ]])
    return menu