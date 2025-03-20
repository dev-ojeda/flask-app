from datetime import timedelta
import os
import secrets
from string import ascii_letters, digits
from dotenv import load_dotenv


load_dotenv()


class Config:
    DEBUG = True
    SECRET_KEY = secrets.token_hex(16)
    SESSION_TYPE = "filesystem"  # Puedes cambiarlo a redis, memcached, etc.
    SESSION_PERMANENT = True
    SESSION_FILE_DIR = "./flask_session/"
    SESSION_USE_SIGNER = False  # Para firmar la cookie de sesión
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=3)
    # PERMANENT_SESSION_LIFETIME = timedelta(days=0, hours=0, minutes=5, microseconds=5.0)
    WTF_CSRF_ENABLED = True
    HOST = "0.0.0.0"
    PORT = 5000


class Generador:
    def __init__(self) -> None:
        pass

    def generador(self, user: str, clave: str) -> None:
        self._user = user
        self._clave = clave
        self._generado: str

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def clave(self):
        return self._clave

    @clave.setter
    def clave(self, value):
        self._clave = value

    def generar_token(self, user_id: str) -> str:
        self.user = user_id
        self._generado = "".join(
            secrets.choice(ascii_letters + self.user + digits) for _ in range(10)
        )
        return self._generado
