from aiogram import types, Dispatcher
from Nails_bot.tgbot.keyboards.reply_main import main_menu


def register_start_bot(dp: Dispatcher):

    @dp.message_handler(commands='start')
    async def bot_echo(message: types.Message):
        await message.answer('Привет! Это тестовый бот, который покажет свою работу. '
                             '\n <b>Выбери что нибудь из кнопок: </b>', reply_markup=main_menu)
