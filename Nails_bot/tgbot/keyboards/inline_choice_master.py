from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_choice_master_data import touch_button_master


def get_menu(idx, way):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Выбрать',
                                                             callback_data=touch_button_master.new(
                                                                 name='hhh',
                                                                 aboute=False,
                                                                 choice=True,
                                                                 id_mast=idx,
                                                                 way=way
                                                             )),
                                        InlineKeyboardButton(text='О мастере',
                                                             callback_data=touch_button_master.new(
                                                                 name='fff',
                                                                 aboute=True,
                                                                 choice=False,
                                                                 id_mast=idx,
                                                                 way=way
                                                             ))
                                    ]
                                ])
    return menu
