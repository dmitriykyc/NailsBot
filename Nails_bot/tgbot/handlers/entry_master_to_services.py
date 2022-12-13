import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline_choice_master import get_menu, get_menu_two
from tgbot.keyboards.inline_choice_master_data import touch_button_master, touch_about_master
from tgbot.keyboards.inline_choice_services import get_done_menu, inline_choose_category, \
    get_menu_choice_services_all, get_menu_service, get_back_menu_datetime
from tgbot.keyboards.inline_choice_services_data import choose_data_and_time, pagination, \
    category_services_touch_button, choice_services_touch_button
from tgbot.keyboards.inline_datatime import get_menu_month, get_menu_day, get_menu_time
from tgbot.keyboards.inline_datetime_data import create_datetime
from tgbot.keyboards.reply_choice_type import get_master_or_serv
from tgbot.services.db_api import db_commands
from tgbot.services.db_api.db_commands import select_service, get_all_masters, select_services_from_category, \
    add_services_to_appointment, select_master
from tgbot.services.db_api.db_gino import on_startup, close_startup
from tgbot.services.db_api.models.appointment_services import Appointment


async def result_message_sum(data):
    '''Функция формирования списка выбранных услуг и суммирования цены'''
    sum_price = 0
    choose_service_list = '\n'
    for ell in data:
        service = await select_service(int(ell))
        choose_service_list += f'🔸 {service.name}\n'
        sum_price += service.price
    return [choose_service_list, sum_price]


async def create_appointment_bd(data_state, call, id_master):
    date_and_time_str = f'{data_state["day"]}.{data_state["month"]}.2022 {data_state["time"]}'
    date_and_time = datetime.datetime.strptime(date_and_time_str, '%d.%m.%Y %H-%M')
    user_id = call['from']['id']
    data_new_appointment = Appointment(user_id=user_id, id_master=int(id_master), datetime=date_and_time)
    await data_new_appointment.create()
    for ell in data_state['services']:
        await add_services_to_appointment(data_new_appointment.id, ell)

    return date_and_time_str


def register_entry_master_to_services(dp: Dispatcher):
    # Нажата кнопка "О Мастере"
    @dp.callback_query_handler(touch_about_master.filter(way='mts'))
    async def message_about_master(call: CallbackQuery, callback_data):
        print(50 * '-')
        await on_startup(dp)
        master = await select_master(id_master=int(callback_data["id"]))
        photo_master = master.photo_master_id

        await call.message.edit_caption(f'Профессиональный мастер, работает в отрасли с 2011 года.\n'
                                        f'Постоянный участник международных выставок и мастерклассов.', reply_markup=get_menu_two(
            master.master_id, 'mts'))
        await close_startup(dp)

    # Нажата кнопка "Записаться"
    @dp.message_handler(text='Записаться')
    async def make_an_entry(message: types.Message):
        print(50 * '-')
        await message.answer('Как Вам удобнее записаться?\n', reply_markup=get_master_or_serv())
        # await message.delete_reply_markup()

    # Нажата кнопка "Выбрать мастера"
    @dp.callback_query_handler(text='choose_master_main')
    async def sent_master(call: CallbackQuery):
        print(50 * '-')
        await on_startup(dp)  # Подключаемся к БД
        masters = await get_all_masters()  # Забираем всех мастеров
        await call.message.delete()
        for ell in masters:
            await call.message.answer_photo(photo=ell.photo_master_id, caption=f'Мастер: <b>{ell.name}</b>\n'
                                                                               f'{ell.disc_master}.\n'
                                                                               f'Рейтинг: 5/5 🌟',
                                            reply_markup=get_menu(ell.master_id, way='mts'))

        await close_startup(dp)  # Закрываем БД

    @dp.callback_query_handler(touch_button_master.filter(aboute='False') and touch_button_master.filter(way='mts'))
    async def touch_inline_button(call: CallbackQuery, callback_data, state: FSMContext):
        print(50 * '-')
        ''' Нажата кнопка "Выбрать" на карточке мастера '''

        id_master = callback_data['id_mast']  # Забираем id мастера
        await on_startup(dp)  # Подключаемся к БД
        await state.update_data(await state.update_data(id_master=id_master))  # Добавляем id в состояние
        date_master = await db_commands.select_master(int(id_master))
        await call.message.answer(f'Вы выбрали мастера - {date_master.name}, всё верно?',
                                  reply_markup=get_done_menu(way='mts'))
        await close_startup(dp)  # Закрываем БД

    @dp.callback_query_handler(create_datetime.filter(way='mts'))
    async def touch_datetime(call: CallbackQuery, callback_data, state: FSMContext):
        print(50 * '-')
        ''' Пробегаемся по выбору года, месяца, даты, времени '''
        await call.answer()  # Закрываем часы
        if callback_data['step'] == 'start':
            await call.message.edit_text('Выберите месяц, когда хотите записаться?')
            await call.message.edit_reply_markup(get_menu_month(callback_data['year'], way='mts'))

        if callback_data['step'] == 'get_month':
            await call.message.edit_text('Выберите число:')
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
            await state.update_data(time=callback_data['time'])
            await state.update_data(month=callback_data['month'])
            await state.update_data(day=callback_data['day'])
            state_data = await state.get_data()
            await on_startup(dp)  # Подключаемся к БД
            data_master = await db_commands.select_master(int(state_data['id_master']))
            await call.message.edit_text(f'🌿 Отлично! Вы выбрали мастера: {data_master.name}\n\n'
                                         f'📌 Дата: {state_data["day"]}.{state_data["month"]}.2022\n\n'
                                         f'🕐 Время: {state_data["time"]}\n\n'
                                         f'Если всё верно, нажмите выбрать услуги 👇',
                                         reply_markup=inline_choose_category('mts'))
            # reply_markup=choose_master())
            await close_startup(dp)  # Закрываем БД


    @dp.callback_query_handler(text='choose_category')
    async def choose_service(call: CallbackQuery, state: FSMContext):
        print(50 * '-')
        '''Обрабатываем Inline Button "Выбрать услугу" '''
        await on_startup(dp)  # Подключаем БД
        category_all = await db_commands.get_all_services_category()  # Тянем из БД все категории
        await state.update_data(services=[])

        await call.message.edit_text(f'Отлично, выберите нужный раздел. \n\n'
                                     f'Можно выбрать несколько услуг.',
                                     reply_markup=get_menu_choice_services_all(0, category_all, 'mts'))
        # await state.update_data(services=[], sum_price=0)  # Задаём состояние
        await close_startup(dp)  # Отключаем БД

    @dp.callback_query_handler(category_services_touch_button.filter(way='mts'))
    async def services_edit_message(call: CallbackQuery, callback_data, state: FSMContext):
        print(50 * '-')
        '''Обрабатывает когда переходим из категории к кнопкам услуг'''
        id_category = int(callback_data['id_category'])  # Забираем категорию
        await on_startup(dp)  # Подключаемся к БД
        services = await select_services_from_category(id_category)  # Тянем все услуги из БД
        state_data = await state.get_data()  # Забираем информацию из состояния
        data_for_text = await result_message_sum(state_data['services'])  # Получаем данные для текста
        await call.message.edit_text(f'Выберите услуги (можно выбрать несколько).\n\n'
                                     f'Ранее выбранные услуги:{data_for_text[0]}\n'
                                     f'Общая сумма: {data_for_text[1]} руб.',
                                     reply_markup=get_menu_service(services, state_data['services'], 'mts'))

        await state.update_data(id_category=id_category)
        await close_startup(dp)

    @dp.callback_query_handler(choice_services_touch_button.filter(way='mts'))
    async def services_edit_message(call: CallbackQuery, callback_data, state: FSMContext):
        print(50 * '-')
        '''Обрабатывает каждое нажатие на кнопках с услугами'''
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
        print(50 * '-')
        '''Обрабатывает кнопку "Назад в категорию"'''
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
        print(50 * '-')
        ''' Обрабатываем кнопку что пользователь набрал себе услуг, хочет записаться '''
        await on_startup(dp)  # Подключаемся к БД
        data_state = await state.get_data()  # Получаем данные из состояния
        id_master = data_state['id_master']
        date_time = await create_appointment_bd(data_state, call, id_master)
        master = await select_master(int(id_master))
        data_for_text = await result_message_sum(data_state['services'])  # Формируем текст
        await call.message.edit_text(f'✅ Вы записаны к мастеру: {master.name} \n'
                                     f'🗓 Дата: {date_time}\n\n'
                                     f'На услуги: \n'
                                     f'{data_for_text[0]}\n\n'
                                     f'💴  Общая стоимость: {data_for_text[1]} руб.\n'
                                     f'📍 Ждём вас по адрему: Г. Москва, Ул. Охотный ряд, д. 1')
        await close_startup(dp)  # Закрываем БД

    @dp.callback_query_handler(choose_data_and_time.filter(way='mts'))
    async def done_choose(call: CallbackQuery, state: FSMContext):
        print(50 * '2-')
        ''' Обрабатываем кнопку что пользователь набрал себе услуг, хочет записаться '''
        await on_startup(dp)  # Подключаемся к БД
        data_state = await state.get_data()  # Получаем данные из состояния
        id_master = data_state['id_master']
        date_time = await create_appointment_bd(data_state, call, id_master)
        master = await select_master(int(id_master))
        data_for_text = await result_message_sum(data_state['services'])  # Формируем текст
        await call.message.edit_text(f'✅ Вы записаны к мастеру: {master.name} \n'
                                     f'🗓 Дата: {date_time}\n\n'
                                     f'На услуги: \n'
                                     f'{data_for_text[0]}\n\n'
                                     f'💴  Общая стоимость: {data_for_text[1]} руб.\n'
                                     f'📍 Ждём вас по адрему: Г. Москва, Ул. Охотный ряд, д. 1')
        await close_startup(dp)  # Закрываем БД

    @dp.callback_query_handler(
        pagination.filter(way='mts'))
    async def answer_callback(call: CallbackQuery, callback_data):
        '''Обрабатывает кнопки далее и назад в категориях'''
        print(50 * '-')
        await call.answer()
        # Создаём пагинацию
        page = int(callback_data['page'])
        back_or_next = callback_data['name']
        if back_or_next == 'next_page':
            page += 1
        else:
            page -= 1
        await on_startup(dp)  # Коннектимся к БД
        category_all = await db_commands.get_all_services_category()  # Тянем все категории
        await call.message.edit_reply_markup(get_menu_choice_services_all(page, category_all, 'mts'))
        await close_startup(dp)  # Отключаемся от БД

