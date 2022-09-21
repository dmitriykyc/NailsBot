from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery

from Nails_bot.tgbot.keyboards.inline_choice_services import get_menu_choice_services, get_menu_choice_services_all, \
    get_menu_service
from Nails_bot.tgbot.keyboards.inline_choice_services_data import choice_services_touch_button, pagination
from Nails_bot.tgbot.keyboards.inline_choice_master import get_menu
from Nails_bot.tgbot.keyboards.inline_choice_master_data import touch_button
from Nails_bot.tgbot.keyboards.inline_datatime import get_menu_years, get_menu_month, get_menu_day, get_menu_time
from Nails_bot.tgbot.keyboards.inline_datetime_data import create_datetime
from Nails_bot.tgbot.keyboards.reply_choice_type import menu_choice_type
from Nails_bot.tgbot.services.db_api.db_commands import get_all_masters, select_master
from Nails_bot.tgbot.services.db_api.db_gino import on_startup



def register_make_an_entry_bot(dp: Dispatcher):

    # Нажата кнопка "Записаться"
    @dp.message_handler(text='Записаться')
    async def make_an_entry(messages: types.Message):
        await messages.answer('Отличненько, выберите как хотите записаться?', reply_markup=menu_choice_type)

    # Нажата кнопка "Выбрать мастера"
    @dp.message_handler(text='Выбрать мастера')
    async def sent_master(messages: types.Message):
        await on_startup(dp)
        masters = await get_all_masters()
        for ell in masters:
            await messages.answer_photo(photo=ell.photo_master_id, caption=f'Мастер: <b>{ell.name}</b>\n'
                                                                           f'{ell.disc_master}.\n'
                                                                           f'Рейтинг: 5/5 🌟',
                                        reply_markup=get_menu(ell.master_id))

    # Нажата кнопка "О Мастере"
    @dp.callback_query_handler(touch_button.filter(aboute='True'))
    async def message_about_master(call: CallbackQuery, callback_data):
        await on_startup(dp)
        master = await select_master(id_master=int(callback_data["id"]))
        photo_master = master.photo_master_id

        await call.message.answer_photo(photo_master, caption=f'Мастер: {master.name}\n'
                                                              f'Рейтинг: 5 из 5\n'
                                                              f'Призвание: {master.disc_master}')

    # Нажата кнопка "Выбрать" на карточке мастера
    @dp.callback_query_handler(touch_button.filter(aboute='False'))
    async def touch_inline_button(call: CallbackQuery, callback_data):
        print(call)
        print(callback_data)
        await call.message.answer('Выберите год: ', reply_markup=get_menu_years())

    # Пробегаемся по выбору года, месяца, даты, времени
    @dp.callback_query_handler(create_datetime.filter())
    async def touch_datetime(call: CallbackQuery, callback_data):
        print(f'@dp.callback_query_handler(create_datetime.filter())\n'
              f'{call=}\n'
              f'{callback_data=}')
        if callback_data['step'] == 'get_year':
            await call.message.edit_text('Выберите Месяц')
            await call.message.edit_reply_markup(get_menu_month(callback_data['year']))
        if callback_data['step'] == 'get_month':
            await call.message.edit_text('Выберите число')
            await call.message.edit_reply_markup(get_menu_day(year=callback_data['year'],
                                                              month=callback_data['month']))
        if callback_data['step'] == 'get_day':
            await call.message.edit_text('Выберите время:')
            await call.message.edit_reply_markup(get_menu_time(year=callback_data['year'],
                                                               month=callback_data['month'],
                                                               day=callback_data['day']))
        if callback_data['step'] == 'get_time':
            await call.message.delete_reply_markup()
            await call.message.answer(f'Отлично! Вы записаны к мастеру Елене на '
                                      f'{callback_data}')


    @dp.message_handler(text='Выбрать услугу')
    async def cange_service(message: types.Message):
        print(get_menu_choice_services_all(0))
        await message.answer('Ok, you need to chnge services', reply_markup=get_menu_choice_services_all(0))

    @dp.callback_query_handler(pagination.filter(name='next_page') | pagination.filter(name='back_page'))
    async def answer_callback(call: CallbackQuery, callback_data):
        # await call.answer(cache_time=60)
        page = int(callback_data['page'])
        back_or_next = callback_data['name']
        if back_or_next == 'next_page':
            page += 1
        else:
            page -= 1
        # print(page)
        await call.message.edit_reply_markup(get_menu_choice_services_all(page))

    @dp.callback_query_handler(choice_services_touch_button.filter())
    async def services_edit_message(call: CallbackQuery, callback_data):
        # print(call)
        # print(callback_data)
        # sum_price = int(callback_data["sum_price"])+int(callback_data["price"])
        await call.message.edit_text(f'Вы выбрали: {callback_data["name"]}\n'
                                     f'Стоимость: <b>1</b>\n'
                                     f'Добавить что нибудь?',
                                     reply_markup=get_menu_service())

    # @dp.callback_query_handler(choice_services_touch_button.filter())
    # async def choice_services(call: CallbackQuery, callback_data):
    #     print(call)
    #     print(callback_data)

