import os
import psycopg2

from dotenv import load_dotenv


def db_connect():
    load_dotenv()
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port=os.getenv("DB_PORT"))
    return connect

def select_master(id_master: int):
    '''Выбрать одного мастера'''
    connect = db_connect()
    cur = connect.cursor()
    sql = f'SELECT master_id, name, photo_master_id, disc_master, working FROM masters WHERE master_id={id_master};'
    cur.execute(sql)
    services_data = cur.fetchone()
    connect.commit()
    connect.close()
    res_master = {'master_id': services_data[0], 
        'name': services_data[1], 
        'photo_master_id': services_data[2],
        'disc_master': services_data[3], 
        'working': services_data[4]}
    return res_master


if __name__ == '__main__':
    select_master(1)

