import os
import psycopg2

from dotenv import load_dotenv


def db_connect():
    load_dotenv()
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port=os.getenv("DB_PORT"))
    return connect

def select_service(id_services: int):
    '''Выбрать одного пользователя'''
    connect = db_connect()
    cur = connect.cursor()
    sql = f'SELECT id, name, price, category_id FROM services WHERE id={id_services};'
    cur.execute(sql)
    services_data = cur.fetchone()
    connect.commit()
    connect.close()
    res_serv = {'id': services_data[0], 
        'name': services_data[1], 
        'price': services_data[2],
        'category_id': services_data[3]}        
    return res_serv

def get_all_list_appointment_from_user(user_id: int):
    connect = db_connect()
    cur = connect.cursor()
    sql = f'SELECT id, user_id, id_master, datetime, active ' \
        f'FROM appointment WHERE user_id={user_id} AND active=TRUE;'
    cur.execute(sql)
    appointment_data = cur.fetchall()
    connect.commit()
    connect.close()
    res_appointment = []
    for appointment in appointment_data:
        res_appo = {'id': appointment[0], 
            'user_id': appointment[1], 
            'id_master': appointment[2],
            'datetime': appointment[3],
            'active':appointment[4]}
        res_appointment.append(res_appo)
    return res_appointment

def get_all_dict_appointment(id_appointment):
    connect = db_connect()
    cur = connect.cursor()
    sql = f'SELECT appointment.id, appointment.user_id, appointment.id_master, appointment.datetime, appointment.active, ' \
        f'appointment_services.id_services FROM appointment INNER JOIN appointment_services ' \
        f'ON appointment_services.id_appointment = appointment.id WHERE appointment.id={id_appointment} '
    cur.execute(sql)
    appointment_data = cur.fetchall()
    connect.commit()
    connect.close()
    res_appointment = []
    if appointment_data:
        res_appo = {'id': appointment_data[0][0], 
                'user_id': appointment_data[0][1], 
                'id_master': appointment_data[0][2],
                'datetime': appointment_data[0][3],
                'active': appointment_data[0][4],
                'id_services': []}
        for appointment in appointment_data:
            res_appo['id_services'].append(appointment[5])
        res_appointment.append(res_appo)
    return res_appointment
    
def edit_active_appointment(id_appointment):
    connect = db_connect()
    cur = connect.cursor()
    sql = f'UPDATE appointment SET active=False WHERE id={id_appointment};'
    cur.execute(sql)
    connect.commit()

if __name__ == '__main__':
    # get_all_list_appointment_from_user(354585871)
    print(get_all_dict_appointment(3))

