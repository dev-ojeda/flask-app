from flask import Flask
from flask_socketio import SocketIO

# Crear una instancia global de SocketIO
socketio: SocketIO = SocketIO(cors_allowed_origins="*")

def create_app() -> Flask:

    """Crea e inicializa la aplicación Flask."""
    app: Flask = Flask(__name__.split('.')[0])
    
    # Configuración de la aplicación
    app.config.from_object('app.config.Config')
    
    # Registrar blueprints
    with app.app_context():
        from app.routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

    # Inicializar SocketIO
    socketio.init_app(app)

    return app