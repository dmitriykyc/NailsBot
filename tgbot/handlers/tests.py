# from aiogram import Dispatcher, types
# from aiogram.dispatcher import FSMContext
# from aiogram.types import InputFile
#
# from Nails_bot.tgbot.misc.states import ChooseServices, FeedbackState
# from Nails_bot.tgbot.services.db_api import db_gino, db_commands
#
# #
# # def register_tests_hendlers(dp: Dispatcher):
# #     @dp.message_handler(content_types=['photo'])
# #     async def answer_hhh(message: types.Message):
# #         photo_id = message.photo[0]['file_id']
# #         print(photo_id)
# #
# #         await message.answer_photo(photo_id, caption='Ооооу еее, это оно. вопрос только как бы замутить поменьше размер')
# #
# #     @dp.message_handler(text='hhh')
# #     async def select_all_masters(message: types.Message):
# #
# #         await db_gino.on_startup(dp)
# #         masters = await db_commands.get_all_masters()
# #         print(masters)
# #
# #         for ell in masters:
# #             await message.answer_photo(ell.photo_master_id, caption=ell.name)
# #             # await message.answer(ell.name + ',' + ell.disc_master)
# #
# #
# #     @dp.message_handler(text='aaa')
# #     async def ssss(message: types.Message, state: FSMContext):
# #         # await state.reset_state()
# #         await message.answer(f'Есть')
# #         await ssss(message, state, text='hrllo')
# #     #
# #     #
# #     @dp.message_handler()
# #     async def ssss(message: types.Message, state: FSMContext, text: str):
# #         await message.answer('ssssssss')
# #         await message.answer(text)
# #         # await state.reset_state()
