from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery

from Nails_bot.tgbot.keyboards.inline_name_user import get_menu_name_user
from Nails_bot.tgbot.keyboards.inline_name_user_data import touch_data_start_name
from Nails_bot.tgbot.keyboards.reply_main import main_menu
from Nails_bot.tgbot.misc.states import CheckName
from Nails_bot.tgbot.services.db_api import db_gino, db_commands


def register_start_bot(dp: Dispatcher):
    @dp.message_handler(commands='start')
    async def start_command(message: types.Message):
        await message.answer('<b>Hello!</b>\n'
                             'Давай знакомиться! Мы делаем ногти\n'
                             'Наш адрес: 3й лихачёвский\n'
                             'Мы классные цены даём')
        name_user = message.from_user["first_name"]
        if name_user:
            await message.answer(f'Можем к Вам обращаться по имени: {message.from_user["first_name"]}?',
                                 reply_markup=get_menu_name_user())
        else:
            await message.answer('Подскажите, как Вас зовут?')
            await CheckName.Q2.set()

    @dp.callback_query_handler(
        touch_data_start_name.filter(choice_button='True') | touch_data_start_name.filter(choice_button='False'))
    async def answer_start_name(call: CallbackQuery, callback_data):
        if callback_data['choice_button'] == 'True':
            # print(callback_data)
            await call.bot.answer_callback_query(call.id)
            await call.message.answer(
                f'Рады что Вы {call.from_user["first_name"]}, можете воспользоваться нашим меню ниже.',
                reply_markup=main_menu)
            await db_gino.on_startup(dp)
            user_id = call.from_user['id']
            user = await db_commands.select_user(id_user=user_id)
            if user:
                await db_commands.update_user(id_user=user_id, name=call.from_user["first_name"])
            else:
                await db_commands.add_user(user_id=user_id, name=call.from_user["first_name"])

        elif callback_data['choice_button'] == 'False':
            await call.message.answer(f'Напишите нам Ваше имя:')
            await CheckName.Q2.set()

    @dp.message_handler(state=CheckName.Q2)
    async def rename_user(message: types.Message, state: FSMContext):

        await db_gino.on_startup(dp)
        new_name = message.text
        user_id = message.from_user['id']
        await state.update_data(new_name_user=new_name)
        user = await db_commands.select_user(id_user=user_id)
        if user:
            await db_commands.update_user(id_user=user_id, name=new_name)
        else:
            await db_commands.add_user(user_id=user_id, name=new_name)
        await state.finish()
        await message.answer(f'{new_name}, очень приятно! \nМожете воспользоваться нашим меню ниже.', reply_markup=main_menu)
