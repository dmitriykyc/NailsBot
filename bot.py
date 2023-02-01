import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.handlers.aboute_us import register_about_us_handlers
from tgbot.handlers.entry_master_to_services import register_entry_master_to_services
from tgbot.handlers.entry_services_to_master import register_entry_services_to_master
from tgbot.handlers.my_account import register_handlers_my_account

from tgbot.handlers.get_photo import register_get_photo
from tgbot.handlers.start_bot import register_start_bot

logging.basicConfig(level=logging.INFO, filename="Nails.log",
                    format=f":--> %(asctime)s %(levelname)s \n (%(lineno)d) - %(message)s ")
load_dotenv()


def register_all_middlewares(dp, config):
    pass
    # dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    pass
    # dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_handlers_my_account(dp)
    register_entry_services_to_master(dp)
    register_entry_master_to_services(dp)
    # register_feedback_handler(dp)
    register_get_photo(dp)
    # # register_hand_about_master(dp)
    # # register_tests_hendlers(dp)
    register_start_bot(dp)
    # # register_make_an_entry_bot(dp)
    register_about_us_handlers(dp)

async def main():
    # config = load_config(".env")

    # storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())

    await bot.set_my_commands([types.BotCommand('start', 'Обновить/перезапустить бота')])

    # register_all_middlewares(dp)
    # register_all_filters(dp)
    register_all_handlers(dp)
    logging.info('Start bot Nails')

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
