from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline_my_account import get_my_account_menu
from tgbot.keyboards.inline_my_account_data import my_account_data
# from tgbot.services.db_api.db_commands import get_all_dict_appointment, get_all_list_appointment_from_user, \
#     edit_active_appointment, select_master
# from tgbot.services.db_api.db_gino import on_startup, close_startup
from tgbot.services.db_api import services_commands_db, masters_commands_db


async def result_message_sum(data):
    '''Функция формирования списка выбранных услуг и суммирования цены'''
    sum_price = 0
    choose_service_list = '\n'
    for ell in data:
        service = services_commands_db.select_service(int(ell))
        choose_service_list += f'🔸 {service["name"]}\n'
        sum_price += service['price']
    return [choose_service_list, sum_price]

def register_handlers_my_account(dp: Dispatcher):
    @dp.message_handler(text='Личный кабинет')
    async def my_account(message: types.Message):
        user_id = message.from_user.id
        all_appointment = services_commands_db.get_all_list_appointment_from_user(user_id) # Забираем активные записи
        if all_appointment == []:
            await message.answer('У Вас нет активных записей')
        else:
            await message.answer('Здесь будет информация о активных записях')
            for ell in all_appointment:
                data_appintment = services_commands_db.get_all_dict_appointment(ell['id'])
                master = masters_commands_db.select_master(data_appintment['id_master'])
                all_services = await result_message_sum(data_appintment['id_services'])
                await message.answer(f'Ваша запись на {data_appintment["datetime"].strftime("%d.%m.%y %H:%M")}\n'
                                     f'Вы записаны к мастеру: {master["name"]}\n'
                                     f'\nВыбранные услуги: {all_services[0]}\n'
                                     f'Сумма: {all_services[1]}',
                                     reply_markup=get_my_account_menu(ell['id']))



    @dp.callback_query_handler(my_account_data.filter())
    async def delete_appointment(call: CallbackQuery, callback_data):
        await call.answer()
        services_commands_db.edit_active_appointment(int(callback_data['id_appointment']))
        await call.message.edit_text('Запись удалена')
