import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

def db_connect():
    load_dotenv()
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port=os.getenv("PORT"))
    return connect

def create_table_users():
    connect = db_connect()
    cur = connect.cursor()
    sql = f'CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, ' \
        f'first_name VARCHAR(255), ' \
        f'user_name VARCHAR(255), ' \
        f'is_active BOOL DEFAULT TRUE, ' \
        f'created_at timestamp DEFAULT NOW(), ' \
        f'updated_at timestamp DEFAULT NOW());'
    cur.execute(sql)
    connect.commit()
    connect.close()
    
def create_table_masters():
    connect = db_connect()
    cur = connect.cursor()
    sql = f'CREATE TABLE IF NOT EXISTS masters (master_id SERIAL PRIMARY KEY, ' \
        f'name VARCHAR(255), ' \
        f'photo_master_id TEXT, ' \
        f'disc_master TEXT, ' \
        f'working BOOL DEFAULT TRUE, ' \
        f'created_at timestamp DEFAULT NOW(), ' \
        f'updated_at timestamp DEFAULT NOW());'
    cur.execute(sql)
    connect.commit()
    connect.close()

def create_table_appointment():
    connect = db_connect()
    cur = connect.cursor()
    sql = f'CREATE TABLE IF NOT EXISTS appointment (' \
        f'id SERIAL PRIMARY KEY, ' \
        f'user_id BIGINT REFERENCES users (id) ON DELETE CASCADE, ' \
        f'id_master INTEGER REFERENCES masters (master_id) ON DELETE CASCADE, ' \
        f'datetime timestamp, ' \
        f'active BOOL DEFAULT TRUE, ' \
        f'created_at timestamp DEFAULT NOW(), ' \
        f'updated_at timestamp DEFAULT NOW());'
    cur.execute(sql)
    connect.commit()
    connect.close()

def create_table_category_services():
    connect = db_connect()
    cur = connect.cursor()
    sql = f'CREATE TABLE IF NOT EXISTS category_services (' \
        f'id SERIAL PRIMARY KEY, ' \
        f'name VARCHAR(255), ' \
        f'active BOOL DEFAULT TRUE, ' \
        f'created_at timestamp DEFAULT NOW(), ' \
        f'updated_at timestamp DEFAULT NOW());'
    cur.execute(sql)
    connect.commit()
    connect.close()
    
def create_table_services():
    connect = db_connect()
    cur = connect.cursor()
    sql = f'CREATE TABLE IF NOT EXISTS services (' \
        f'id SERIAL PRIMARY KEY, ' \
        f'name VARCHAR(255), ' \
        f'price INTEGER DEFAULT 0, ' \
        f'category_id INTEGER REFERENCES category_services (id) ON DELETE CASCADE, ' \
        f'created_at timestamp DEFAULT NOW(), ' \
        f'updated_at timestamp DEFAULT NOW());'
    cur.execute(sql)
    connect.commit()
    connect.close()

def create_table_appointment_services():
    connect = db_connect()
    cur = connect.cursor()
    sql = f'CREATE TABLE IF NOT EXISTS appointment_services (' \
        f'id SERIAL PRIMARY KEY, ' \
        f'id_appointment INTEGER REFERENCES appointment (id) ON DELETE CASCADE, ' \
        f'id_services INTEGER REFERENCES services (id) ON DELETE CASCADE, ' \
        f'created_at timestamp DEFAULT NOW(), ' \
        f'updated_at timestamp DEFAULT NOW());'
    cur.execute(sql)
    connect.commit()
    connect.close()

def drop_table(name):
    connect = db_connect()
    cur = connect.cursor()
    sql = f'DROP TABLE "{name}" CASCADE;'
    cur.execute(sql)
    connect.commit()
    connect.close()
    

if __name__ == '__main__':
    # create_table_users()
    # create_table_masters()
    # create_table_appointment()
    # create_table_category_services()
    # create_table_services()
    # create_table_appointment_services()
    pass
