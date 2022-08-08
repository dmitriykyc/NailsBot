from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery

from Nails_bot.tgbot.keyboards.inline_choice_master import get_menu
from Nails_bot.tgbot.keyboards.inline_choice_master_data import touch_button
from Nails_bot.tgbot.keyboards.reply_choice_type import menu_choice_type


def register_make_an_entry_bot(dp: Dispatcher):

    @dp.message_handler(text='Записаться')
    async def make_an_entry(messages: types.Message):
        await messages.answer('Отличненько, выберите как хотите записаться?', reply_markup=menu_choice_type)


    @dp.message_handler(text='Выбрать мастера')
    async def sent_master(messages: types.Message):
        names = {'Sonya': 1, 'Chinara': 2, 'Nura': 3, 'Jacka': 4, 'Sonya2': 5, 'Chinara2': 6, 'Nura2': 7, 'Jacka2': 8, 'Sonya3': 9, 'Chinara3': 10}
        for ell in names:
            await messages.answer(f'Мастер: <b>{ell}</b>\n'
                                      f'Мастер ногтевого сервиса.\n'
                                      f'Рейтинг: 5/5 🌟', reply_markup=get_menu(names[ell]))

    @dp.callback_query_handler(touch_button.filter(aboute='True'))
    async def touch_inline_button(call: CallbackQuery, callback_data):
        await call.bot.answer_callback_query(call.id)
        await call.message.answer('This is right')
        print(callback_data)
        print(call)
        print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')