from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_choice_master_data import touch_button


def get_menu(idx):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Выбрать',
                                                             callback_data=touch_button.new(
                                                                 name='hhh',
                                                                 aboute=False,
                                                                 choice=True,
                                                                 id=idx
                                                             )),
                                        InlineKeyboardButton(text='О мастере',
                                                             callback_data=touch_button.new(
                                                                 name='fff',
                                                                 aboute=True,
                                                                 choice=False,
                                                                 id=idx
                                                             ))
                                    ]
                                ])
    return menu
