import asyncio

from Nails_bot.tgbot.services.db_api import db_commands
from Nails_bot.tgbot.services.db_api.db_gino import db, config
from Nails_bot.tgbot.services.db_api.models.masters import Master


async def db_test():
    print(1)
    await db.set_bind(config.db.postgres_uri)
    print(2)
    # await db.gino.drop_all()
    # print(3)
    # await db.gino.create_all()
    print(4)
    # user = await Master.get(1)
    # await user.delete()
    # await db_commands.delete_mater(2)
    # masters = await db.all(Master.query)
    # print(masters[0].name)
    # await db_commands.add_master(name='Elena', photo_master_id='AgACAgIAAxkBAAICUGL7m8o7bSVrAfOS9Ty-ZJaBKXxkAAKYvzEb9NzhS6wyYW2w1w6IAQADAgADcwADKQQ', disc_master='Greate master')
    # await db_commands.add_master(name='Elena', photo_master_id='AgACAgIAAxkBAAICUmL7m9dSCYhYH215S9AbtVveBNGdAAKovzEb9NzhSyOkAAFaXBkm_gEAAwIAA3MAAykE', disc_master='Really greate master')
    # await db_commands.add_master(name='Elena', photo_master_id='AgACAgIAAxkBAAICVGL7m-raAAFdAAFMMZUUlH32nO1fu6cAAqq_MRv03OFL7SqpXPbJZhYBAAMCAANzAAMpBA', disc_master='Greate master 2')
    # await db_commands.add_master(name='Elena', photo_master_id='AgACAgIAAxkBAAICVmL7m_uaOIU7oiy3yFVlZFflGv51AAKsvzEb9NzhSy6dbE42xFT8AQADAgADcwADKQQ', disc_master='Greate master3')
    # await db_commands.add_user(1, 'dmitriy')
    # print(5)
    # # # users = await quick_commands.select_all_users()
    # # # print(users)
    # # user = await quick_commands.select_user(1)
    # # print(user)

loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
