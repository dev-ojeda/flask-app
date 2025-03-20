from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_session import Session

# from flask_login import LoginManager

session = Session()
bootstrap = Bootstrap()
csrf = CSRFProtect()


def create_app() -> Flask:
    """
    The function `create_app` initializes a Flask application, registers blueprints, and initializes
    global instances of SocketIO and login manager.
    :return: The function `create_app()` is returning an instance of a Flask application.
    """

    """Crea e inicializa la aplicación Flask."""

    app: Flask = Flask(__name__.split(".")[0])
    # Crear una instancia global de SocketIO
    # Configuración de la aplicación
    app.config.from_object("app.config.Config")
    # Registrar blueprints
    with app.app_context():
        from app.routes import main as main_blueprint

        app.register_blueprint(main_blueprint)
        from app.model import user as user_blueprint

        app.register_blueprint(user_blueprint)

    session.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    return app
