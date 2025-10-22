import bcrypt  #type:ignore
from serializers import UserRegister


def hash_password(raw_password: str):
    encoded_password = raw_password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_password, salt).decode()


def match_password(raw_password: str, encoded_password: str):
    raw_password = raw_password.encode()
    return bcrypt.checkpw(raw_password, encoded_password.encode())


class Response:
    def __init__(self, message, status_code=200):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.message} = {self.status_code}"


def login_required(func):
    def wrapper(*args, **kwargs):
        from session import Session
        session = Session()

        if session:
            return func(*args, **kwargs)
        else:
            return Response("login required", 401)

    return wrapper


def validate_user(dto: UserRegister):
    assert dto.username, "Username must be required"
    assert dto.password, "Password must be required"


def is_admin(func):
    def wrapper(*args, **kwargs):
        from session import Session
        session = Session()

        if not session.session:
            return Response('Login required', 401)
        
        if session.session.role != 'admin':
            return Response('Only admin user can be changed', 403)
        
        return func(*args, **kwargs)
    return wrapper
