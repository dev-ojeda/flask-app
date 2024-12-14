from flask import Flask

def create_app():
    """Crea e inicializa la aplicación Flask."""
    app = Flask(__name__.split('.')[0])
    
    # Configuración de la aplicación
    app.config.from_object('app.config.Config')

    # Registrar rutas
    with app.app_context():
        from .routes.routes_app import main
        app.register_blueprint(main)

    return app