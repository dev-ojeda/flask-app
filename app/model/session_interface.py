import uuid
from flask.sessions import SessionInterface, SessionMixin


class UsernameSession(dict, SessionMixin):
    """Clase de sesión vinculada a un nombre de usuario."""

    def __init__(self, username=None, initial=None):
        super().__init__(initial or {})
        self.username = username
        self.modified = False


class UsernameSessionInterface(SessionInterface):
    """Interfaz de sesión personalizada que usa el username como identificador."""

    storage = {}

    def open_session(self, app, request):
        # Obtener el nombre de usuario desde la cookie
        username = request.cookies.get("username")
        if username and username in self.storage:
            # Retornar la sesión existente para el usuario
            return UsernameSession(username, initial=self.storage[username])

        # Crear una nueva sesión si no existe
        return UsernameSession()

    def save_session(self, app, session, response):
        if not session:
            # Eliminar sesión si está vacía
            username = session.username
            if username and username in self.storage:
                del self.storage[username]
            response.delete_cookie("username")
            return

        # Guardar la sesión en el almacenamiento en memoria
        if session.username:
            self.storage[session.username] = dict(session)
            response.set_cookie("username", session.username)
        else:
            # Si no hay un username asociado, generar uno temporal
            temp_username = str(uuid.uuid4())
            session.username = temp_username
            self.storage[temp_username] = dict(session)
            response.set_cookie("username", temp_username)
