import os
from socketio import Server, WSGIApp
import eventlet
from dotenv import load_dotenv
from flask import Flask
from icecream import ic
from app import create_app
from app.config import Config as conf


load_dotenv()
app: Flask = create_app()
app.secret_key = conf.SECRET_KEY
sio = Server(cors_allowed_origins="*", async_mode="eventlet")
app = WSGIApp(sio, app)


def main() -> None:
    """
    The main function logs a message and starts a Socket.IO server on localhost port 5000.
    """
    ic("Servidor Socket.IO ejecutándose en http://localhost:5000")
    ic("Servidor Socket.IO ejecutándose en http://127.0.0.1:5000")
    # app.run(conf.host, int(conf.port))
    eventlet.wsgi.server(eventlet.listen((conf.HOST, int(conf.PORT))), app)


# The `if __name__ == "__main__":` block in Python is a common idiom used to ensure that the code
# inside it is only executed if the script is run directly, and not imported as a module into another
# script.
if __name__ == "__main__":
    main()
