from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from Nails_bot.tgbot.keyboards.inline_feedback import get_menu_feedback
from Nails_bot.tgbot.misc.states import FeedbackState


def register_feedback_handler(dp: Dispatcher):

    @dp.message_handler(text='Написать отзыв')
    async def feedback(message: types.Message):
        await message.answer('Здравствуйте, Елена!\nВы 16.09 посещали наш салон у мастера Людмилы.\nПожалуйста, оцените работу мастера и нашего салона:',
                             reply_markup=get_menu_feedback())
        await FeedbackState.Q1.set()

    @dp.callback_query_handler(state=FeedbackState.Q1)
    async def get_feedback(call: CallbackQuery, callbackdata):
        await call.message.answer("Отлично! Теперь введите ваш адрес.")
        print(callbackdata)
