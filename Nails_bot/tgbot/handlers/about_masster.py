'''
Описание мастера
'''
from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from Nails_bot.masters import masters
from Nails_bot.tgbot.keyboards.inline_choice_master_data import touch_button


def register_hand_about_master(dp: Dispatcher):
    @dp.callback_query_handler(touch_button.filter(aboute='True'))
    async def message_about_master(call: CallbackQuery, callback_data):
        photo = 'AgACAgIAAxkBAAIBU2LxKLKoyJRXXEF04Nv-5P0uXc74AAL6vDEbCJWQS1GiecgXhNyQAQADAgADcwADKQQ'
        id_master = callback_data["id"]
        await call.message.answer_photo(photo, caption=f'Мастер: Мастер 1\n'
                                                       f'Рейтинг: 5 из 5\n'
                                                       f'Призвание: Боженька манирюра')
