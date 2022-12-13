from asyncpg import UniqueViolationError
import psycopg2
from dotenv import load_dotenv
import os

# from tgbot.services.db_api.models.appointment_services import AppointmentServices, Appointment
# from tgbot.services.db_api.models.category_services import CategoryServices, Services
# from tgbot.services.db_api.models.masters import Master
# from tgbot.services.db_api.models.user import User

def db_connect():
    load_dotenv()
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port=os.getenv("DB_PORT"))
    return connect




# async def add_user(user_id: int, name: str):
#     '''Добавление пользователя'''
#     try:
#         user = User(user_id=user_id, name=name)
#         await user.create()
#     except UniqueViolationError:
#         print(f'User {user_id=}, {name=}, is not append')


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


# async def select_user(id_user: int):
#     '''Выбрать одного пользователя'''
#     user = await User.get(id_user)
#     return user


# async def select_master(id_master: int):
#     '''Выбрать одного пользователя'''
#     master = await Master.get(id_master)
#     return master


# async def update_user(id_user: int, name: str):
#     '''Обновить юзера'''
#     user = await User.get(id_user)
#     await user.update(name=name).apply()


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


# async def select_service(id_services: int):
#     ''''''
#     service = await Services.get(id_services)
#     return service


async def add_services_to_appointment(id_appointment: int, id_services: int):
    try:
        data = AppointmentServices(id_appointment=id_appointment, id_services=id_services)
        await data.create()
    except:
        print(f'AppointmentServices {id_appointment=}, is not append')


async def add_appointment(user_id: int, id_master: int, datetime):
    data = Appointment(user_id=user_id, id_master=id_master, datetime=datetime)
    await data.create()


# async def get_all_dict_appointment(id_appointment):
#     appointment = await Appointment.get(id_appointment)
#     id_master = appointment.id_master
#     datetime = appointment.datetime
#     services = await AppointmentServices.query.where(AppointmentServices.id_appointment == id_appointment).gino.all()
#     all_services_list = [ell.id_services for ell in services]
#     active = appointment.active
#     result_appointment = {'id_master': id_master,
#                           'datetime': datetime,
#                           'services': all_services_list,
#                           'active': active}

#     return result_appointment

# async def get_all_list_appointment_from_user(user_id: int):
#     all_appointment = await Appointment.query.where(and_(
#         Appointment.user_id == user_id,
#         Appointment.active)).gino.all()
#     res_ell = [ell.id for ell in all_appointment]
#     return res_ell

# async def edit_active_appointment(id_appointment):
#     appointment = await Appointment.get(id_appointment)
#     await appointment.update(active=False).apply()

if __name__ == '__main__':
    db_connect()


