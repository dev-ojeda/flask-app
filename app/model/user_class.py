# Modelo de usuario

from flask_login import UserMixin
from flask.sessions import SessionMixin


# The class `User` in Python takes an `id` parameter and initializes an object with that id.
class User(UserMixin):

    def __init__(self, username: str) -> None:
        self.id = username


class CustomSession(SessionMixin):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def clear(self):
        self.data.clear()
