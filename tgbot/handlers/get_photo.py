
from asyncio.log import logger
import logging
from aiogram import Dispatcher, types
from aiogram.types import ContentType


def register_get_photo(dp: Dispatcher):

    @dp.message_handler(content_types=ContentType.PHOTO)
    async def get_photo(message: types.Message):
        # await message.photo[-1].download(destination_dir= r'D:\Programming\TG_BOTS\Nails_bot\Nails_bot\tgbot\media\masters_photo')
        mess_id = message.photo[0]['file_id']
        logging.info(mess_id)
        await message.answer('Спасибо')
        # await message.answer_photo(mess_id, caption='You are send to me this photo')
