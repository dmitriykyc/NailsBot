from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery

from Nails_bot.tgbot.keyboards.inline_choice_master_data import touch_button_master
# from Nails_bot.tgbot.keyboards.inline_choice_services import get_menu_choice_services, get_menu_choice_services_all, \
#     get_menu_service, get_done_menu, choose_master
# from Nails_bot.tgbot.keyboards.inline_choice_services_data import choice_services_touch_button, pagination, \
#     category_services_touch_button, choose_data_and_time
from Nails_bot.tgbot.keyboards.inline_choice_master import get_menu
from Nails_bot.tgbot.keyboards.inline_datatime import get_menu_years, get_menu_month, get_menu_day, get_menu_time
from Nails_bot.tgbot.keyboards.inline_datetime_data import create_datetime
from Nails_bot.tgbot.keyboards.reply_choice_type import menu_choice_type
from Nails_bot.tgbot.misc.states import ChooseServices
from Nails_bot.tgbot.services.db_api import db_commands
from Nails_bot.tgbot.services.db_api.db_commands import get_all_masters, select_master, select_services_from_category, \
    select_service
from Nails_bot.tgbot.services.db_api.db_gino import on_startup, close_startup


async def result_message_sum(data):
    '''Функция формирования списка выбранных услуг и суммирования цены'''
    sum_price = 0
    choose_service_list = '\n'
    for ell in data:
        service = await select_service(int(ell))
        choose_service_list += f'🔸 {service.name}\n'
        sum_price += service.price
    return [choose_service_list, sum_price]


def register_make_an_entry_bot(dp: Dispatcher):
    #     # Нажата кнопка "Записаться"
    # @dp.message_handler(text='Записаться')
    # async def make_an_entry(messages: types.Message):
    #     await messages.answer('Отличненько, выберите как хотите записаться?', reply_markup=menu_choice_type)

    # # Нажата кнопка "Выбрать мастера", тут будут все мастера, к которым будут подтягиваться даты свободные
    # @dp.message_handler(text='Выбрать мастера')
    # async def sent_master(messages: types.Message):
    #     await on_startup(dp)
    #     masters = await get_all_masters()
    #     for ell in masters:
    #         await messages.answer_photo(photo=ell.photo_master_id, caption=f'Мастер: <b>{ell.name}</b>\n'
    #                                                                        f'{ell.disc_master}.\n'
    #                                                                        f'Рейтинг: 5/5 🌟',
    #                                     reply_markup=get_menu(ell.master_id))
    #
    #     await close_startup(dp)

    # Нажата кнопка "О Мастере"
    @dp.callback_query_handler(touch_button_master.filter(aboute='True'))
    async def message_about_master(call: CallbackQuery, callback_data):
        await on_startup(dp)
        master = await select_master(id_master=int(callback_data["id"]))
        photo_master = master.photo_master_id

        await call.message.answer_photo(photo_master, caption=f'Мастер: {master.name}\n'
                                                              f'Рейтинг: 5 из 5\n'
                                                              f'Призвание: {master.disc_master}')
        await close_startup(dp)

    # # Нажата кнопка "Выбрать" на карточке мастера или переход из callback после выбоа услуг
    # @dp.callback_query_handler(touch_button.filter(aboute='False') | choose_data_and_time.filter(go_d_t='True'))
    # async def touch_inline_button(call: CallbackQuery, callback_data, state: FSMContext):
    #     print(callback_data)
    #     id_master = callback_data['id_mast']
    #     await state.update_data(id_master=id_master)
    #     await call.message.answer('Выберите год: ', reply_markup=get_menu_years())
    #
    # # Пробегаемся по выбору года, месяца, даты, времени
    # @dp.callback_query_handler(create_datetime.filter())
    # async def touch_datetime(call: CallbackQuery, callback_data, state: FSMContext):
    #     print(f'@dp.callback_query_handler(create_datetime.filter())\n'
    #           f'{call=}\n'
    #           f'{callback_data=}')
    #     if callback_data['step'] == 'get_year':
    #         await call.message.edit_text('Выберите Месяц')
    #         await call.message.edit_reply_markup(get_menu_month(callback_data['year']))
    #     if callback_data['step'] == 'get_month':
    #         await call.message.edit_text('Выберите число')
    #         await call.message.edit_reply_markup(get_menu_day(year=callback_data['year'],
    #                                                           month=callback_data['month']))
    #     if callback_data['step'] == 'get_day':
    #         await call.message.edit_text('Выберите время:')
    #         await call.message.edit_reply_markup(get_menu_time(year=callback_data['year'],
    #                                                            month=callback_data['month'],
    #                                                            day=callback_data['day']))
    #
    #     if callback_data['step'] == 'get_time':
    #         await call.message.delete_reply_markup()
    #         await state.update_data(time=callback_data['month'])
    #         await state.update_data(month=callback_data['month'])
    #         await state.update_data(day=callback_data['day'])
    #         result_data = await state.get_data()
    #         print(result_data)
    #         if result_data['id_master'] == '':
    #             await call.message.answer(f'Отлично! Вы выбрали:\n'
    #                                       f'Дата: {result_data["day"]}.{result_data["month"]}\n\n'
    #                                       f'Нажмите выбрать мастера.',
    #                                       reply_markup=choose_master())
    #         else:
    #             await call.message.answer(f'Отлично! Вы записаны к мастеру 1212 на '
    #                                       f'\n\n {await state.get_data()}')

    # @dp.message_handler(text='Выбрать услугу')
    # async def choose_service(message: types.Message, state: FSMContext):
    #     print(await state.get_data())
    #     await on_startup(dp)
    #     category_all = await db_commands.get_all_services_category()
    #     await message.answer(f'Выберите нужный раздел:', reply_markup=get_menu_choice_services_all(0, category_all))
    #     await state.update_data(services=[], sum_price=0)
    #     await close_startup(dp)

    # @dp.callback_query_handler(pagination.filter(name='next_page') | pagination.filter(name='back_page'))
    # async def answer_callback(call: CallbackQuery, callback_data):
    #     '''Обрабатывает кнопки далее и назад в категориях'''
    #     await call.answer()
    #     page = int(callback_data['page'])
    #     back_or_next = callback_data['name']
    #     if back_or_next == 'next_page':
    #         page += 1
    #     else:
    #         page -= 1
    #     await on_startup(dp)
    #     category_all = await db_commands.get_all_services_category()
    #     await call.message.edit_reply_markup(get_menu_choice_services_all(page, category_all))
    #     await close_startup(dp)

    # @dp.callback_query_handler(category_services_touch_button.filter())
    # async def services_edit_message(call: CallbackQuery, callback_data, state: FSMContext):
    #     '''Обрабатывает когда переходим из категории к кнопкам услуг'''
    #     id_category = int(callback_data['id_category'])
    #     await on_startup(dp)
    #     services = await select_services_from_category(id_category)
    #     call_data = await state.get_data()
    #     data_for_text = await result_message_sum(call_data['services'])
    #     await call.message.edit_text(f'Выберите услугу.\n'
    #                                  f'Выбраны услуги:{data_for_text[0]}\n'
    #                                  f'Общая сумма: {data_for_text[1]} руб.',
    #                                  reply_markup=get_menu_service(services, call_data['services']))
    #
    #     await state.update_data(id_category=id_category)
    #     await close_startup(dp)

    # @dp.callback_query_handler(choice_services_touch_button.filter())
    # async def services_edit_message(call: CallbackQuery, callback_data, state: FSMContext):
    #     '''Обрабатывает каждое нажатие на кнопках с услугами'''
    #     all_services = await state.get_data('services')
    #     list_services = all_services["services"]
    #     if int(callback_data['id']) in list_services:
    #         list_services.remove(int(callback_data['id']))
    #     else:
    #         list_services.append(int(callback_data['id']))
    #     await state.update_data(services=list_services)
    #     all_services = await state.get_data()
    #     print(all_services)
    #     next_all_serv = await state.get_data('services')
    #     data = await state.get_data()
    #     await call.answer()
    #
    #     call_data = await state.get_data()
    #     id_category = call_data['id_category']
    #
    #     await on_startup(dp)
    #     services = await select_services_from_category(id_category)
    #     data_for_text = await result_message_sum(call_data['services'])
    #     print(data_for_text)
    #     await call.message.edit_text(text=f'Выберите услугу.\n'
    #                                       f'Выбраны услуги:{data_for_text[0]}\n'
    #                                       f'Общая сумма: {data_for_text[1]} руб.',
    #                                  reply_markup=get_menu_service(services, call_data['services']))
    #     await close_startup(dp)

    # @dp.callback_query_handler(text='back_to_category')
    # async def choose_service2(call: CallbackQuery, state: FSMContext):
    #     '''Обрабатывает кнопку "Назад в категорию"'''
    #     await on_startup(dp)
    #     category_all = await db_commands.get_all_services_category()
    #     call_data = await state.get_data()
    #     data_for_text = await result_message_sum(call_data['services'])
    #     await call.message.edit_text(f'Выбраны услуги:{data_for_text[0]}\n'
    #                                  f'Общая сумма: {data_for_text[1]} руб.\n',
    #                                  reply_markup=get_menu_choice_services_all(0, category_all))
    #
    #     await close_startup(dp)

    # @dp.callback_query_handler(choose_data_and_time.filter())
    # async def done_choose(call: CallbackQuery, callback_data, state: FSMContext):
    #     await on_startup(dp)
    #     call_data = await state.get_data()
    #     data_for_text = await result_message_sum(call_data['services'])
    #     await call.message.edit_text(f'Выбраны услуги:{data_for_text[0]}\n'
    #                                  f'Общая сумма: {data_for_text[1]} руб.\n',
    #                                  reply_markup=get_done_menu())
    #     await close_startup(dp)

    # # Тут будут все мастера, которые подходят под дату и время.
    # @dp.callback_query_handler(text='choose_master')
    # async def choose_master_after_all(call: CallbackQuery):
    #     await on_startup(dp)
    #     masters = await get_all_masters()
    #     for ell in masters:
    #         await call.message.answer_photo(photo=ell.photo_master_id, caption=f'Мастер: <b>{ell.name}</b>\n'
    #                                                                        f'{ell.disc_master}.\n'
    #                                                                        f'Рейтинг: 5/5 🌟',
    #                                         reply_markup=get_menu(ell.master_id))
    #
    #     await close_startup(dp)

