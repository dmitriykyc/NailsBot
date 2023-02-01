import os
import psycopg2

from dotenv import load_dotenv


def db_connect():
    load_dotenv()
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port=os.getenv("PORT"))
    return connect

def add_user(user_id: int, first_name: str, username: str):
    '''Добавление пользователя'''
    connect = db_connect()
    cur = connect.cursor()
    sql = f"INSERT INTO users (id, first_name, user_name) VALUES ({user_id}, '{first_name}', '{username}');"
    cur.execute(sql)
    connect.commit()
    connect.close()

def select_user(user_id: int):
    '''Выбрать одного пользователя'''
    connect = db_connect()
    cur = connect.cursor()
    sql = f'SELECT id, first_name, user_name FROM users WHERE id={user_id};'
    cur.execute(sql)
    user_data = cur.fetchone()
    connect.commit()
    connect.close()
    return user_data

def update_user(user_id: int, name: str):
    '''Обновить юзера'''
    connect = db_connect()
    cur = connect.cursor()
    sql = f"UPDATE users SET first_name='{name}' WHERE id={user_id};"
    cur.execute(sql)
    connect.commit()
    connect.close()

    

if __name__ == '__main__':
    pass