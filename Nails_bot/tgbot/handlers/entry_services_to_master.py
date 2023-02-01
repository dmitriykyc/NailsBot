import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from tgbot.keyboards.inline_choice_master import get_menu, get_menu_two
from tgbot.keyboards.inline_choice_master_data import touch_button_master, touch_about_master
from tgbot.keyboards.inline_choice_services import get_menu_choice_services_all, get_menu_service, \
    get_done_menu, choose_master
from tgbot.keyboards.inline_choice_services_data import pagination, category_services_touch_button, \
    choice_services_touch_button, choose_data_and_time
from tgbot.keyboards.inline_datatime import get_menu_month, get_menu_day, get_menu_time
from tgbot.keyboards.inline_datetime_data import create_datetime

from tgbot.services.db_api import masters_commands_db, services_commands_db


async def result_message_sum(data):
    '''Функция формирования списка выбранных услуг и суммирования цены'''
    sum_price = 0
    choose_service_list = '\n'
    for ell in data:
        service = services_commands_db.select_service(int(ell))
        choose_service_list += f'🔸 {service["name"]}\n'
        sum_price += service["price"]
    return [choose_service_list, sum_price]


async def create_appointment_bd(data_state, call, id_master):
    print(50*'1-1')
    date_and_time_str = f'{data_state["day"]}.{data_state["month"]}.2022 {data_state["time"]}:00'
    date_and_time = datetime.datetime.strptime(date_and_time_str, '%d.%m.%Y %H:%M')
    user_id = call['from']['id']

    # data_new_appointment = Appointment(user_id=user_id, id_master=int(id_master), datetime=date_and_time)
    # await data_new_appointment.create()
    data_new_appointment = services_commands_db.insert_appointment(
        user_id=user_id, id_master=int(id_master), datetime=date_and_time)
    for ell in data_state['services']:
        services_commands_db.add_services_to_appointment(data_new_appointment, ell)

    return date_and_time_str


def register_entry_services_to_master(dp: Dispatcher):
    print(50*'10')
    # Нажата кнопка "О Мастере"
    @dp.callback_query_handler(touch_about_master.filter(way='stm'))
    async def message_about_master(call: CallbackQuery, callback_data):
        master = masters_commands_db.select_master(id_master=int(callback_data["id"]))
        # photo_master = master['photo_master_id']
        await call.message.edit_caption(f'Описание мастера, на сколько он хорош', reply_markup=get_menu_two(
            master.master_id, 'stm'))

    # Пробегаемся по выбору года, месяца, даты, времени
    @dp.callback_query_handler(create_datetime.filter(way='stm'))
    async def touch_datetime(call: CallbackQuery, callback_data, state: FSMContext):

        print(50 * '9')

        await call.answer()  # Закрываем часы
        if callback_data['step'] == 'start':
            await call.message.edit_text('Выберите месяц, когда хотите записаться?')
            await call.message.edit_reply_markup(get_menu_month(callback_data['year'], way='stm'))

        if callback_data['step'] == 'get_month':
            await call.message.edit_text('Выберите число')
            await call.message.edit_reply_markup(get_menu_day(year=callback_data['year'],
                                                              month=callback_data['month'], way='stm'))
        if callback_data['step'] == 'get_day':
            await call.message.edit_text('Выберите время:')
            await call.message.edit_reply_markup(get_menu_time(year=callback_data['year'],
                                                               month=callback_data['month'],
                                                               day=callback_data['day'], way='stm'))

        if callback_data['step'] == 'get_time':  # Если всё пройдено, собираем данные
            # await call.message.delete_reply_markup()
            await state.update_data(time=callback_data['month'])
            await state.update_data(month=callback_data['month'])
            await state.update_data(day=callback_data['day'])
            state_data = await state.get_data()

            data_for_text = await result_message_sum(state_data['services'])  # Получаем данные для текста
            await call.message.edit_text(f'Отлично! Вы выбрали услуги:\n'
                                         f'{data_for_text[0]}\n\n'
                                         f'Общая сумма: {data_for_text[1]}\n\n'
                                         f'Дата: {state_data["day"]}.{state_data["month"]}.2022\n\n'
                                         f'Нажмите выбрать мастера.',
                                         reply_markup=choose_master())

    @dp.callback_query_handler(text='choose_master')
    async def sent_masters(call: CallbackQuery):
        print(50 * '8')

        masters = masters_commands_db.get_all_masters()  # Получаем всех мастеров
        for ell in masters:
            await call.message.answer_photo(photo=ell["photo_master_id"], caption=f'Мастер: <b>{ell["name"]}</b>\n'
                                                                               f'{ell["disc_master"]}.\n'
                                                                               f'Рейтинг: 5/5 🌟',
                                            reply_markup=get_menu(ell["master_id"], 'stm'))


    # Нажата кнопка "Выбрать" на карточке мастера
    @dp.callback_query_handler(touch_button_master.filter(aboute='False') and touch_button_master.filter(way='stm'))
    async def touch_inline_button(call: CallbackQuery, callback_data, state: FSMContext):
        print(50 * '7')
        id_master = callback_data['id_mast']
        await state.update_data(id_master=id_master)
        data_state = await state.get_data()
        date_time = await create_appointment_bd(data_state, call, id_master)

        data_for_text = await result_message_sum(data_state['services'])  # Получаем данные для текста
        master = masters_commands_db.select_master(int(data_state['id_master']))
        await call.message.answer(f'✅ Вы записаны к мастеру: {master["name"]} \n'
                                  f'🗓 Дата: {date_time}\n\n'
                                  f'На услуги: \n'
                                  f'{data_for_text[0]}\n\n'
                                  f'💴  Общая стоимость: {data_for_text[1]} руб.\n'
                                  f'📍 Ждём вас по адрему: Г. Москва, Ул. Охотный ряд, д. 1 ')

    @dp.callback_query_handler(text='choose_service_main')
    async def choose_service(call: CallbackQuery, state: FSMContext):
        '''Обрабатываем Reply Button "Выбрать услугу" '''
        print(100 * '6')
        category_all = services_commands_db.get_all_services_category()  # Тянем из БД все категории
        data_state = await state.get_data()
        await call.message.edit_text(f'Отлично, выберите нужный раздел. \n\n'
                             f'Можно выбрать несколько услуг.',
                             reply_markup=get_menu_choice_services_all(0, category_all, 'stm'))
        await state.update_data(services=[], sum_price=0)  # Задаём состояние

    @dp.callback_query_handler(pagination.filter(way='stm'))
    async def answer_callback(call: CallbackQuery, callback_data):
        '''Обрабатывает кнопки далее и назад в категориях'''
        print(50 * '5')
        await call.answer()
        # Создаём пагинацию
        page = int(callback_data['page'])
        back_or_next = callback_data['name']
        if back_or_next == 'next_page':
            page += 1
        else:
            page -= 1
        category_all = services_commands_db.get_all_services_category()  # Тянем все категории
        await call.message.edit_reply_markup(get_menu_choice_services_all(page, category_all, 'stm'))

    @dp.callback_query_handler(category_services_touch_button.filter(way='stm'))
    async def services_edit_message(call: CallbackQuery, callback_data, state: FSMContext):
        '''Обрабатывает когда переходим из категории к кнопкам услуг'''
        print(50 * '4')
        id_category = int(callback_data['id_category'])  # Забираем категорию

        services = services_commands_db.select_services_from_category(id_category)  # Тянем все услуги из БД
        state_data = await state.get_data()  # Забираем информацию из состояния
        data_for_text = await result_message_sum(state_data['services'])  # Получаем данные для текста
        await call.message.edit_text(f'Выберите услуги (Можно несколько).\n\n'
                                     f'Ранее выбранные услуги:{data_for_text[0]}\n'
                                     f'Общая сумма: {data_for_text[1]} руб.',
                                     reply_markup=get_menu_service(services, state_data['services'], 'stm'))

        await state.update_data(id_category=id_category)

    @dp.callback_query_handler(choice_services_touch_button.filter(way='stm'))
    async def services_edit_message(call: CallbackQuery, callback_data, state: FSMContext):
        '''Обрабатывает каждое нажатие на кнопках с услугами'''
        print(50 * '3')
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

        services = services_commands_db.select_services_from_category(id_category)  # Забираем все услуги
        data_for_text = await result_message_sum(state_data['services'])  # Формируем текст
        await call.message.edit_text(text=f'Выберите услугу.\n\n'
                                          f'Ранее выбранные услуги:{data_for_text[0]}\n'
                                          f'Общая сумма: {data_for_text[1]} руб.',
                                     reply_markup=get_menu_service(services, state_data['services'], 'stm'))

    @dp.callback_query_handler(text='back_to_category_stm')
    async def choose_service2(call: CallbackQuery, state: FSMContext):
        '''Обрабатывает кнопку "Назад в категорию"'''
        print(50 * '2')

        category_all = services_commands_db.get_all_services_category()  # Тянем из БД все категории
        call_data = await state.get_data()  # Забираем данные из состояния
        data_for_text = await result_message_sum(call_data['services'])  # Формируем текст
        await call.message.edit_text(f'Выбраны услуги:{data_for_text[0]}\n'
                                     f'Общая сумма: {data_for_text[1]} руб.\n',
                                     reply_markup=get_menu_choice_services_all(0, category_all, 'stm'))


    @dp.callback_query_handler(choose_data_and_time.filter(way='stm'))
    async def done_choose(call: CallbackQuery, callback_data, state: FSMContext):
        ''' Обрабатываем кнопку что пользователь набрал себе услуг, хочет записаться '''
        print(50 * '1')

        state_data = await state.get_data()  # Получаем данные из состояния
        data_for_text = await result_message_sum(state_data['services'])  # Формируем текст
        await call.message.edit_text(f'Выбраны услуги:{data_for_text[0]}\n'
                                     f'Общая сумма: {data_for_text[1]} руб.\n',
                                     reply_markup=get_done_menu(way='stm'))
