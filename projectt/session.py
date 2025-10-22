from models import User
from utils import login_required



class Session:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = None
        return cls._instance

    def add_session(self, user):
        """Store the logged-in user in the session."""
        self.session = user

    def check_session(self):
        """Return the current session user if exists."""
        return self.session


