import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from Nails_bot.tgbot.handlers.aboute_us import register_about_us_handlers
from Nails_bot.tgbot.handlers.entry_master_to_services import register_entry_master_to_services
from Nails_bot.tgbot.handlers.entry_services_to_master import register_entry_services_to_master
from Nails_bot.tgbot.handlers.feedback import register_feedback_handler
from Nails_bot.tgbot.handlers.get_photo import register_get_photo
# from Nails_bot.tgbot.handlers.make_an_entry import register_make_an_entry_bot
from Nails_bot.tgbot.handlers.my_account import register_handlers_my_account
from Nails_bot.tgbot.handlers.start_bot import register_start_bot
# from Nails_bot.tgbot.handlers.tests import register_tests_hendlers
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter

# from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    pass
    # dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_handlers_my_account(dp)
    register_entry_services_to_master(dp)
    register_entry_master_to_services(dp)
    register_feedback_handler(dp)
    register_get_photo(dp)
    # register_hand_about_master(dp)
    # register_tests_hendlers(dp)
    register_start_bot(dp)
    # register_make_an_entry_bot(dp)
    register_about_us_handlers(dp)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    await bot.set_my_commands([types.BotCommand('start', 'Обновить/перезапустить бота')])

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

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
        logger.error("Bot stopped!")
