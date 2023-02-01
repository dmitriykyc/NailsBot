from asyncio import run_coroutine_threadsafe
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

def get_all_masters():
    '''Забрать всех мастеров'''
    connect = db_connect()
    cur = connect.cursor()
    sql = f'SELECT master_id, name, photo_master_id, disc_master, working FROM masters WHERE working=TRUE;'
    cur.execute(sql)
    masters_data = cur.fetchall()
    connect.commit()
    connect.close()
    res_masters = []
    for master in masters_data:
        res_master = {}
        res_master['master_id'] = master[0]
        res_master['name'] = master[1]
        res_master['photo_master_id'] = master[2]
        res_master['disc_master'] = master[3]
        res_master['working'] = master[4]
        res_masters.append(res_master)
    return res_masters


if __name__ == '__main__':
    print(get_all_masters())

