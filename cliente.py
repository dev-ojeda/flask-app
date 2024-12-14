# flask_socketio_app.py
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Servidor Flask-SocketIO corriendo"

# Manejar mensajes recibidos desde Tkinter
@socketio.on('mensaje_tkinter')
def handle_message(data):
    print(f"Mensaje recibido desde Tkinter: {data}")
    emit('respuesta_flask', {'mensaje': 'Mensaje recibido correctamente'}, broadcast=True)

# Iniciar el servidor
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, use_reloader=False)