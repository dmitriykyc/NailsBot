from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_name_user_data import touch_data_start_name


def get_menu_name_user():
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Да, это я!',
                                                             callback_data=touch_data_start_name.new(
                                                                 choice_button=True
                                                             )),
                                        InlineKeyboardButton(text='Нет, изменить...',
                                                             callback_data=touch_data_start_name.new(
                                                                 choice_button=False
                                                             ))
                                    ]
                                ])
    return menu
