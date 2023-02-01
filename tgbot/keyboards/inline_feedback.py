from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nails_bot.tgbot.keyboards.inline_feedback_data import touch_data_feedback


def get_menu_feedback():
    menu = InlineKeyboardMarkup(row_width=5,
                                inline_keyboard=[[
                                    InlineKeyboardButton(text='1⭐️', callback_data=touch_data_feedback.new('1')),
                                    InlineKeyboardButton(text='2⭐️', callback_data=touch_data_feedback.new('2')),
                                    InlineKeyboardButton(text='3⭐️', callback_data=touch_data_feedback.new('3')),
                                    InlineKeyboardButton(text='4⭐️', callback_data=touch_data_feedback.new('4')),
                                    InlineKeyboardButton(text='5⭐️', callback_data=touch_data_feedback.new('5'))
                                ]])

    return menu