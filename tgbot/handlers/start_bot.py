import asyncio
from asyncio.log import logger
from cgitb import text
from hashlib import new
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline_name_user import get_menu_name_user
from tgbot.keyboards.inline_name_user_data import touch_data_start_name
from tgbot.keyboards.reply_main import main_menu
from tgbot.misc.states import CheckName

# from tgbot.services.db_api import db_gino, db_commands
from tgbot.services.db_api import user_commands_db
from tgbot.services.db_api import create_tables_bd


def register_start_bot(dp: Dispatcher):
    # Обрабатываем команду старт
    @dp.message_handler(commands='start')
    async def start_command(message: types.Message, state: FSMContext):
        logger.info('[v] Новый пользователь:\n'
              f'{message.from_user}\n'
              f'-------------------------------------------')
        await message.answer_photo(
            photo='AgACAgIAAxkBAAIN02M_PRukNN6IGUi5vdDvKAPaGglYAAIsxDEbTZH4SYrwWgTo2e8iAQADAgADcwADKgQ',
            caption=f'Приветствуем Вас в чат боте салона: <b>«Иль де Франс»</b>💅\n\n'
                    f'Мы находимы по адресу:\n'
                    f'📍 г.Москва, ул.Охотный ряд, д. 1\n\n'
                    f'В этом чат боте Вы можете записаться на услуги, управлять своими записями, '
                    f'так же здесь будут появляться самые сочные предложения от нашего салона '
                    f'и мы обязательно напомним о Вашем посещении накануне.\n\n'
                    f'Приятного пользования!\nНо, давайте для начала познакомимся👇')

        name_user = message.from_user.first_name
        username = message.from_user.username
        if name_user:
            await message.answer(
                f'Вам будет комфортно, если мы будем обращаться к Вам по имени: {name_user}?',
                reply_markup=get_menu_name_user())
        else:
            await message.answer('Пожалуйста, напишите как Вас зовут?👇')
            await CheckName.Q2.set()
            await asyncio.sleep(60)
            if await state.get_state():
                await state.finish()


    # Проверка имени пользователя из профиля в телеграм
    @dp.callback_query_handler(
        touch_data_start_name.filter(choice_button='True') | touch_data_start_name.filter(choice_button='False'))
    async def answer_start_name(call: CallbackQuery, callback_data):
        if callback_data['choice_button'] == 'True':
            await call.bot.answer_callback_query(call.id)
            await call.message.answer(
                f'Очень приятно, {call.from_user["first_name"]}, можете воспользоваться нашим меню ниже.\n\n'
                f'(Если меню спряталось, нажмите 🎛, рядом с кнопкой микрофона)',
                reply_markup=main_menu)
            user_id = call.from_user['id']
            user = user_commands_db.select_user(user_id)
            print(user)
            if user:
                user_commands_db.update_user(id_user=user_id, name=call.from_user["first_name"])
            else:
                user_commands_db.add_user(user_id=user_id, 
                    first_name=call.from_user.first_name, 
                    username=call.from_user.username)

        elif callback_data['choice_button'] == 'False':
            await call.message.answer(f'Напишите нам Ваше имя:')
            await CheckName.Q2.set()

    # Изменение имени, проверить состояния, нужно ли их вообще использовать
    @dp.message_handler(state=CheckName.Q2)
    async def rename_user(message: types.Message, state: FSMContext):
        await state.finish()
        new_name = message.text
        user_id = message.from_user['id']
        await state.update_data(new_name_user=new_name)
        user = user_commands_db.select_user(user_id)
        if user:
            user_commands_db.update_user(user_id, name=new_name)
        else:
            user_commands_db.add_user(user_id=user_id, 
                    first_name=new_name, 
                    username=message.from_user.username)
        await message.answer(f'{new_name}, очень приятно! \nМожете воспользоваться нашим меню ниже.\n\n'
                             f'(Если меню спряталось, нажмите 🎛, рядом с кнопкой микрофона)',
                             reply_markup=main_menu)

    @dp.message_handler(text='Создай таблицы')
    async def create_table(message: types.message):
        create_tables_bd.create_table_appointment()
        create_tables_bd.create_table_appointment_services()
        create_tables_bd.create_table_category_services()
        create_tables_bd.create_table_masters()
        create_tables_bd.create_table_services()
        create_tables_bd.create_table_users()