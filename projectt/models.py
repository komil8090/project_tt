from enum import Enum
from dataclasses import dataclass


class TodoType(Enum):
    PERSONAL = 'personal'
    WORKING  = 'working'


class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'






@dataclass
class User():
    username : str
    password : str
    id : int | None = None
    role : UserRole = UserRole.USER.value
    created_at : None = None


    @staticmethod
    def from_tuple(user_data : tuple):
        return User(
            id = user_data[0],
            username = user_data[1],
            password = user_data[2],
            role = user_data[3],
            created_at = user_data[4]
            
        )



@dataclass
class Todo():
    title : str
    user_id : int
    description : str | None = None
    todo_type : TodoType = TodoType.PERSONAL.value
    created_at : None = None
    id : int | None = None





