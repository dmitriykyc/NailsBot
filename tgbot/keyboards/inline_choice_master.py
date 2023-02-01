from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline_choice_master_data import touch_button_master, touch_about_master


def get_menu(idx, way):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Выбрать',
                                                             callback_data=touch_button_master.new(
                                                                 aboute=False,
                                                                 choice=True,
                                                                 id_mast=idx,
                                                                 way=way
                                                             )),
                                        InlineKeyboardButton(text='О мастере',
                                                             callback_data=touch_about_master.new(
                                                                 id=idx,
                                                                 way=way
                                                             ))
                                    ]
                                ])
    return menu


def get_menu_two(idx, way):
    menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Выбрать',
                                                             callback_data=touch_button_master.new(
                                                                 aboute=False,
                                                                 choice=True,
                                                                 id_mast=idx,
                                                                 way=way
                                                             ))
                                    ]
                                ])
    return menu

