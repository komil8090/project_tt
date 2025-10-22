import psycopg2  #type:ignore
import os
from dotenv import load_dotenv #type:ignore
from utils import hash_password
from models import UserRole,TodoType



load_dotenv()


db_info = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}


conn = psycopg2.connect(**db_info)
cur = conn.cursor()


def auto_commit(func):
    def wrapper(*args,**kwargs):
        result = func(*args,**kwargs)
        conn.commit()
        return result
    return wrapper


@auto_commit
def create_user_table():
    user_query = ''' create table users(
            id serial primary key,
            username  varchar(255) not null,
            password varchar(255) not null,
            role varchar(15) default 'user',
            created_at timestamptz default now()
    );
    '''

    cur.execute(user_query)



@auto_commit
def create_todo_table():
    todo_query = ''' create table todos(
            id serial primary key,
            title varchar(255) not null,
            description text,
            todo_type varchar(255) default 'personal',
            user_id int references users(id),
            created_at timestamptz default now()
    )
    '''

    cur.execute(todo_query)






@auto_commit
def insert_admin():
    cur.execute("SELECT * FROM users WHERE username = %s", ('twis',))
    if cur.fetchone():
        print("Admin already exists ✅")
        return
    insert_admin_query = '''INSERT INTO users(username, password, role)
    VALUES (%s, %s, %s)'''
    data = ('twis', hash_password('twis123'), UserRole.ADMIN.value)
    cur.execute(insert_admin_query, data)
    print("Admin successfully added ✅")


