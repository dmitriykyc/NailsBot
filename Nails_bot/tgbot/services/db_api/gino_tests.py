import asyncio
from datetime import datetime
from sqlalchemy import and_

from Nails_bot.tgbot.services.db_api import db_commands
from Nails_bot.tgbot.services.db_api.db_commands import add_services_to_appointment, add_appointment, select_master, \
    get_all_dict_appointment, get_all_list_appointment_from_user
from Nails_bot.tgbot.services.db_api.db_gino import db, config
from Nails_bot.tgbot.services.db_api.models.appointment_services import Appointment, AppointmentServices
from Nails_bot.tgbot.services.db_api.models.category_services import Services, CategoryServices
from Nails_bot.tgbot.services.db_api.models.masters import Master


async def db_test():
    print(1)
    await db.set_bind(config.db.postgres_uri)
    print(2)
    # await db.gino.drop()
    # print(3)
    await db.gino.create_all()
    # print(3)
    # date = datetime.now()
    # # await add_appointment(user_id=354585871, id_master=5, datetime=data)
    # # await add_services_to_appointment(3, 1)
    # data = Appointment(user_id=354585871, id_master=5, datetime=date)
    # await data.create()
    # print(data.id)

    # all_data = await get_all_dict_appointment(1)
    # print(all_data)
    # await add_services_to_appointment(3, 6)

    # service = await Services.get(1)
    # service = await Services.get(Services.id == 1)
    # print(service)
    # await user.delete()
    # await db_commands.delete_mater(2)
    # masters = await db.all(Master.query)
    # print(masters[0].name)
    # await db_commands.add_master(name='Elena', photo_master_id='AgACAgIAAxkBAAICUGL7m8o7bSVrAfOS9Ty-ZJaBKXxkAAKYvzEb9NzhS6wyYW2w1w6IAQADAgADcwADKQQ', disc_master='Greate master')
    # await db_commands.add_category_srvices(name='Мужской зал', active=True)
    # await db_commands.add_services(name='Руки до локтя', price=400, category_id=9)
    # await db_commands.add_services(name='Руки полностью', price=600, category_id=9)
    # await db_commands.add_services(name='Ноги до колен', price=600, category_id=9)
    # await db_commands.add_services(name='Ноги полностью', price=1200, category_id=9)
    # await db_commands.add_services(name='Бикини трусики', price=500, category_id=9)
    # await db_commands.add_services(name='Бикини глубокое', price=900, category_id=9)
    # await db_commands.add_services(name='Верхняя губа', price=100, category_id=9)
    # await db_commands.add_services(name='Подмышки', price=300, category_id=9)
    # # await db_commands.add_user(1, 'dmitriy')
    # print(5)
    # **********
    # groups = await db_commands.select_services_from_category(1)
    # for i in groups:
    #     print(i.name)
    # **********
    # # # users = await quick_commands.select_all_users()
    # # # print(users)
    # user = await quick_commands.select_user(1)
    # # print(user)


loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
