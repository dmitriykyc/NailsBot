from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery

from Nails_bot.tgbot.keyboards.inline_choice_master import get_menu
from Nails_bot.tgbot.keyboards.inline_choice_master_data import touch_button
from Nails_bot.tgbot.keyboards.reply_choice_type import menu_choice_type
from Nails_bot.tgbot.services.db_api.db_commands import get_all_masters, select_master
from Nails_bot.tgbot.services.db_api.db_gino import on_startup
from aiogram_calendar import SimpleCalendar, DialogCalendar, dialog_cal_callback


def register_make_an_entry_bot(dp: Dispatcher):
    @dp.message_handler(text='Записаться')
    async def make_an_entry(messages: types.Message):
        await messages.answer('Отличненько, выберите как хотите записаться?', reply_markup=menu_choice_type)

    @dp.message_handler(text='Выбрать мастера')
    async def sent_master(messages: types.Message):
        await on_startup(dp)
        masters = await get_all_masters()
        for ell in masters:
            await messages.answer_photo(photo=ell.photo_master_id, caption=f'Мастер: <b>{ell.name}</b>\n'
                                                                           f'{ell.disc_master}.\n'
                                                                           f'Рейтинг: 5/5 🌟',
                                        reply_markup=get_menu(ell.master_id))

    @dp.callback_query_handler(touch_button.filter(aboute='True'))
    async def message_about_master(call: CallbackQuery, callback_data):
        await on_startup(dp)
        master = await select_master(id_master=int(callback_data["id"]))
        photo_master = master.photo_master_id

        await call.message.answer_photo(photo_master, caption=f'Мастер: {master.name}\n'
                                                              f'Рейтинг: 5 из 5\n'
                                                              f'Призвание: {master.disc_master}')










    # Календарь из сторонней библиоткеи
    # @dp.callback_query_handler(touch_button.filter(aboute='False'))
    # async def touch_inline_button(call: CallbackQuery, callback_data):
    #     '''Календарь из Inline кнопок'''
    #
    #     # await call.message.answer("Вы выбрали мастера: Елена\n"
    #     #                           "Выберите дату посещения:", reply_markup=await SimpleCalendar().start_calendar())
    #     DialogCalendar.months = ["Янв", "Фев", "Март", "Апр", "Май", "Июнь", "Июль", "Авг", "Сент", "Окт", "Нояб", "Дек"]
    #     await call.message.answer("Вы выбрали мастера: Елена\n"
    #                               "Выберите дату посещения:", reply_markup=await DialogCalendar().start_calendar())
    #     # await call.bot.answer_callback_query(call.id)
    #     # await call.message.answer('This is right')
    #     # print(callback_data)
    #     # print(call)
    #     # print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    #
    # @dp.callback_query_handler(dialog_cal_callback.filter())
    # async def process_dialog_calendar(callback_query: CallbackQuery, callback_data):
    #     selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    #     if selected:
    #         await callback_query.message.answer(
    #             f'You selected {date.strftime("%d/%m/%Y")}'
    #         )
