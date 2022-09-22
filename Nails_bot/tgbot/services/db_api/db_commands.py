from asyncpg import UniqueViolationError

from Nails_bot.tgbot.services.db_api.models.category_services import CategoryServices, Services
from Nails_bot.tgbot.services.db_api.models.masters import Master
from Nails_bot.tgbot.services.db_api.models.user import User3


async def add_user(user_id: int, name: str):
    '''Добавление пользователя'''
    try:
        user = User3(user_id=user_id, name=name)
        await user.create()
    except UniqueViolationError:
        print(f'User {user_id=}, {name=}, is not append')


async def add_master(name: str, photo_master_id: str, disc_master: str):
    '''Добавление мастера'''
    try:
        master = Master(name=name, photo_master_id=photo_master_id, disc_master=disc_master)
        await master.create()
    except UniqueViolationError:
        print(f'Master {name=}, is not append')


async def delete_mater(id_master: int):
    '''Удаление мастера'''
    master = await Master.get(id_master)
    if master:
        await master.delete()


async def get_all_masters():
    '''Забрать всех мастеров'''
    return await Master.query.gino.all()


async def select_user(id_user: int):
    '''Выбрать одного пользователя'''
    user = await User3.get(id_user)
    return user


async def select_master(id_master: int):
    '''Выбрать одного пользователя'''
    master = await Master.get(id_master)
    return master


async def update_user(id_user: int, name: str):
    '''Обновить юзера'''
    user = await User3.get(id_user)
    await user.update(name=name).apply()

async def update_master(master_id: int, photo_master_id: str):
    '''Обновить мастера'''
    user = await Master.get(master_id)
    await user.update(photo_master_id=photo_master_id).apply()


async def add_category_srvices(name: str, active: bool):
    '''Добавление категории услуг'''
    try:
        category = CategoryServices(name=name, active=active)
        await category.create()
    except UniqueViolationError:
        print(f'Category {name=}, is not append')

async def add_services(name: str, price: int, category_id: int):
    '''Добавление усолуг к категории'''
    try:
        services = Services(name=name, price=price, category_id=category_id)
        await services.create()
    except:
        print(f'Category {name=}, is not append')

async def get_all_services_category():
    '''Забрать все категории услуг'''
    return await CategoryServices.query.gino.all()

async def select_services_from_category(id_category: int):
    '''Выборка услуг из категории'''
    services = await Services.query.where(Services.category_id == id_category).gino.all()
    return services