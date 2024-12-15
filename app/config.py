import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración de la aplicación."""
    debug = True  # Habilitar el modo de depuración
    gitbug_token = os.getenv("GITHUB_TOKEN")
    secret_key = os.getenv("SECRET_KEY")  # Clave secreta para sesiones
    sonar_key = os.getenv("SONAR_TOKEN")
    host = os.getenv("HOST")
    port = os.getenv("PORT")