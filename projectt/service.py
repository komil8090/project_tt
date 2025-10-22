from session import Session
from utils import Response, match_password, hash_password, login_required,is_admin
from db import cur, auto_commit
from models import User, TodoType
from service import auto_commit
session = Session()




def login(username : str, password : str):
    user = session.check_session()
    if user:
        return Response('you already logged in',404)
    
    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username,(username,))


    user_data = cur.fetchone()

    if not user_data:
        return Response('user not found',404)
    

    user = User.from_tuple(user_data)
    if not match_password(password, user.password):
        return Response('password wrong',404)
    
    session.add_session(user)
    return Response('you successfully logged in')


def log_out():
    if session.session:
        session.session = None
        return Response('You have successfully logged out', 200)
    
    return Response('No active session found', 404)


@auto_commit
def register(username, password, role):
    cur.execute("""
        INSERT INTO users (username, password, role)
        VALUES (%s, %s, %s)
    """, (username, hash_password(password), role))

    return Response("User registered successfully", 201)




@login_required
@is_admin
@auto_commit
def add_todo(title: str, description: str | None = None):
    insert_todo_query = '''
    INSERT INTO todos (title, user_id, todo_type, description)
    VALUES (%s, %s, %s, %s)
    '''
    user = session.session
    cur.execute(insert_todo_query, (title, user.id, TodoType.PERSONAL.value, description))
    return Response('✅ Todo successfully inserted', 201)




@login_required
@is_admin
@auto_commit
def update_admin_role(user_id):
    all_users_query = '''select * from users where  role = 'user' ;'''
    cur.execute(all_users_query)
    users = cur.fetchall()
    for user in users:
        print(user)

    update_admin_role_query = '''update users set role = 'admin' where id = %s ;'''
    cur.execute(update_admin_role_query, (user_id,))
    return Response('user successfully updates',202)








@login_required
@is_admin
@auto_commit
def get_user_todo():
    user = session.session  # Hozirgi foydalanuvchi
    
    query = """SELECT id, title, description, todo_type FROM todos WHERE user_id = %s;
    """
    cur.execute(query, (user.id,))
    todos = cur.fetchall()

    if not todos:
        return Response("You have no todos yet.", 200)

    print("\n ---- Todos ----")
    for todo in todos:
        todo_id, title, description, todo_type = todo
        print(f"ID: {todo_id} | Title: {title} | Description: {description or '-'} | Type: {todo_type}")

    return Response("Todos successfully retrieved.", 200)