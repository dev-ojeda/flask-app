import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración de la aplicación."""
    debug = True  # Habilitar el modo de depuración
    secret_key = os.getenv("SECRET_KEY")  # Clave secreta para sesiones
    host = os.getenv("HOST")
    port = os.getenv("PORT")