from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from Nails_bot.tgbot.keyboards.inline_choice_master import get_menu
from Nails_bot.tgbot.keyboards.inline_choice_master_data import touch_button_master
from Nails_bot.tgbot.keyboards.inline_choice_services import get_done_menu, inline_choose_category, \
    get_menu_choice_services_all, get_menu_service
from Nails_bot.tgbot.keyboards.inline_choice_services_data import choose_data_and_time, pagination, \
    category_services_touch_button, choice_services_touch_button
from Nails_bot.tgbot.keyboards.inline_datatime import get_menu_month, get_menu_day, get_menu_time
from Nails_bot.tgbot.keyboards.inline_datetime_data import create_datetime
from Nails_bot.tgbot.keyboards.reply_choice_type import menu_choice_type
from Nails_bot.tgbot.services.db_api import db_commands
from Nails_bot.tgbot.services.db_api.db_commands import select_service, get_all_masters, select_services_from_category
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


def register_entry_master_to_services(dp: Dispatcher):
    # Нажата кнопка "Записаться"
    @dp.message_handler(text='Записаться')
    async def make_an_entry(messages: types.Message):
        await messages.answer('Отличненько, выберите как хотите записаться?', reply_markup=menu_choice_type)

    # Нажата кнопка "Выбрать мастера", тут будут все мастера, к которым будут подтягиваться даты свободные
    @dp.message_handler(text='Выбрать мастера')
    async def sent_master(messages: types.Message):
        await on_startup(dp)
        masters = await get_all_masters()
        for ell in masters:
            await messages.answer_photo(photo=ell.photo_master_id, caption=f'Мастер: <b>{ell.name}</b>\n'
                                                                           f'{ell.disc_master}.\n'
                                                                           f'Рейтинг: 5/5 🌟',
                                        reply_markup=get_menu(ell.master_id, way='mts'))

        await close_startup(dp)

    # Нажата кнопка "Выбрать" на карточке мастера
    @dp.callback_query_handler(touch_button_master.filter(aboute='False') and touch_button_master.filter(way='mts'))
    async def touch_inline_button(call: CallbackQuery, callback_data, state: FSMContext):

        print('----' * 100)

        id_master = callback_data['id_mast']
        await state.update_data(await state.update_data(id_master=id_master))
        await call.message.answer(f'Вы выбрали мастера - {id_master}, теперь выбрать дату и выбрать макстера',
                                  reply_markup=get_done_menu(way='mts'))

        # await state.update_data(id_master=id_master)
        # data_state = await state.get_data()
        #
        # await on_startup(dp)  # Подключаемся к БД
        # data_for_text = await result_message_sum(data_state['services'])  # Получаем данные для текста
        # master = await db_commands.select_master(int(data_state['id_master']))
        # await call.message.answer(f'Вы записаниы к мастеру: {master.name} \n'
        #                           f'Дата: {data_state["day"]}{data_state["month"]}.2022\n'
        #                           f'На услуги: \n'
        #                           f'{data_for_text[0]}\n\n'
        #                           f'Общая стоимость: {data_for_text[1]} руб.\n\n'
        #                           f'Ждём вас по адрему: Г. Москва, Ул. Ростокино 15А ')
        # await close_startup(dp)  # Закрываем БД

        # Пробегаемся по выбору года, месяца, даты, времени

    @dp.callback_query_handler(create_datetime.filter(way='mts'))
    async def touch_datetime(call: CallbackQuery, callback_data, state: FSMContext):

        print('-' * 100)

        await call.answer()  # Закрываем часы
        if callback_data['step'] == 'start':
            await call.message.edit_text('Выберите месяц, когда хотите записаться?')
            await call.message.edit_reply_markup(get_menu_month(callback_data['year'], way='mts'))

        if callback_data['step'] == 'get_month':
            await call.message.edit_text('Выберите число')
            await call.message.edit_reply_markup(get_menu_day(year=callback_data['year'],
                                                              month=callback_data['month'],
                                                              way='mts'))
        if callback_data['step'] == 'get_day':
            await call.message.edit_text('Выберите время:')
            await call.message.edit_reply_markup(get_menu_time(year=callback_data['year'],
                                                               month=callback_data['month'],
                                                               day=callback_data['day'],
                                                               way='mts'))

        if callback_data['step'] == 'get_time':  # Если всё пройдено, собираем данные
            # await call.message.delete_reply_markup()
            await state.update_data(time=callback_data['month'])
            await state.update_data(month=callback_data['month'])
            await state.update_data(day=callback_data['day'])
            state_data = await state.get_data()
            await on_startup(dp)  # Подключаемся к БД
            # data_for_text = await result_message_sum(state_data['services'])  # Получаем данные для текста
            await call.message.edit_text(f'Отлично! Вы выбрали мастера: Леночка\n'
                                         f'Дата: xx.xx.2022\n\n'
                                         f'Нажмите выбрать услуги:',
                                         reply_markup=inline_choose_category())
            # reply_markup=choose_master())
            await close_startup(dp)  # Закрываем БД

    @dp.callback_query_handler(text='choose_category')
    async def choose_service(call: CallbackQuery, state: FSMContext):
        '''Обрабатываем Inline Button "Выбрать услугу" '''

        print('-' * 100)

        await on_startup(dp)  # Подключаем БД
        category_all = await db_commands.get_all_services_category()  # Тянем из БД все категории
        await state.update_data(services=[])

        await call.message.answer(f'Отлично, выберите нужный раздел. \n\n'
                             f'Можно выбрать несколько услуг.',
                             reply_markup=get_menu_choice_services_all(0, category_all, 'mts'))
        # await state.update_data(services=[], sum_price=0)  # Задаём состояние
        await close_startup(dp)  # Отключаем БД

    @dp.callback_query_handler(category_services_touch_button.filter(way='mts'))
    async def services_edit_message(call: CallbackQuery, callback_data, state: FSMContext):
        '''Обрабатывает когда переходим из категории к кнопкам услуг'''

        print('-' * 100)

        id_category = int(callback_data['id_category'])  # Забираем категорию
        await on_startup(dp)  # Подключаемся к БД
        services = await select_services_from_category(id_category)  # Тянем все услуги из БД
        state_data = await state.get_data()  # Забираем информацию из состояния
        data_for_text = await result_message_sum(state_data['services'])  # Получаем данные для текста
        await call.message.edit_text(f'Выберите услугу.\n\n'
                                     f'Ранее выбранные услуги:{data_for_text[0]}\n'
                                     f'Общая сумма: {data_for_text[1]} руб.',
                                     reply_markup=get_menu_service(services, state_data['services'], 'mts'))

        await state.update_data(id_category=id_category)
        await close_startup(dp)

    @dp.callback_query_handler(choice_services_touch_button.filter(way='mts'))
    async def services_edit_message(call: CallbackQuery, callback_data, state: FSMContext):
        '''Обрабатывает каждое нажатие на кнопках с услугами'''

        print('-' * 100)

        all_services = await state.get_data()
        list_services = all_services["services"]  # Забираем все выбранные услуги

        # При повторном нажатии убирает услугу из состояния, при первом - добавляет.
        if int(callback_data['id']) in list_services:
            list_services.remove(int(callback_data['id']))
        else:
            list_services.append(int(callback_data['id']))

        await state.update_data(services=list_services)  # Обновляем список в состоянии
        await call.answer()  # отключаем часики с кнопки

        state_data = await state.get_data()  # Снова получаем данные из состояния
        id_category = state_data['id_category']  # Забираем категорию
        await on_startup(dp)  # Подключаемся к БД
        services = await select_services_from_category(id_category)  # Забираем все услуги
        data_for_text = await result_message_sum(state_data['services'])  # Формируем текст
        await call.message.edit_text(text=f'Выберите услугу.\n\n'
                                          f'Ранее выбранные услуги:{data_for_text[0]}\n'
                                          f'Общая сумма: {data_for_text[1]} руб.',
                                     reply_markup=get_menu_service(services, state_data['services'], 'mts'))
        await close_startup(dp)  # Закрываем БД

    @dp.callback_query_handler(text='back_to_category_mts')
    async def choose_service2(call: CallbackQuery, state: FSMContext):
        '''Обрабатывает кнопку "Назад в категорию"'''

        print('-' * 100)

        await on_startup(dp)  # Подключаемся к БД
        category_all = await db_commands.get_all_services_category()  # Тянем из БД все категории
        call_data = await state.get_data()  # Забираем данные из состояния
        data_for_text = await result_message_sum(call_data['services'])  # Формируем текст
        await call.message.edit_text(f'Выбраны услуги:{data_for_text[0]}\n'
                                     f'Общая сумма: {data_for_text[1]} руб.\n',
                                     reply_markup=get_menu_choice_services_all(0, category_all, 'mts'))
        await close_startup(dp)  # Закрываем БД

    # @dp.callback_query_handler(choose_data_and_time.filter())
    # async def done_choose(call: CallbackQuery, callback_data, state: FSMContext):
    #     ''' Обрабатываем кнопку что пользователь набрал себе услуг, хочет записаться '''
    #
    #     print('*' * 100)
    #
    #     await on_startup(dp)  # Подключаемся к БД
    #     state_data = await state.get_data()  # Получаем данные из состояния
    #     data_for_text = await result_message_sum(state_data['services'])  # Формируем текст
    #     await call.message.edit_text(f'Выбраны услуги:{data_for_text[0]}\n'
    #                                  f'Общая сумма: {data_for_text[1]} руб.\n',
    #                                  reply_markup=get_done_menu(way='mts'))
    #     await close_startup(dp)  # Закрываем БД
    #
    #
    @dp.callback_query_handler(text='finish_mts')
    async def done_choose(call: CallbackQuery, state: FSMContext):
        ''' Обрабатываем кнопку что пользователь набрал себе услуг, хочет записаться '''

        print('1-' * 100)

        await on_startup(dp)  # Подключаемся к БД
        state_data = await state.get_data()  # Получаем данные из состояния
        data_for_text = await result_message_sum(state_data['services'])  # Формируем текст
        await call.message.edit_text(f'Спасибо! Вы записаны! Вывести информацию о записи')
        await close_startup(dp)  # Закрываем БД

