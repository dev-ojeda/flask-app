from flask import Flask, render_template
from flask_socketio import SocketIO, Namespace, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Definir un namespace personalizado
class ChatNamespace(Namespace):
    def on_connect(self):
        print('Cliente conectado al namespace /chat')

    def on_disconnect(self):
        print('Cliente desconectado del namespace /chat')

    def on_mensaje(self, data):
        print(f'Mensaje recibido: {data}')
        emit('respuesta', f'Servidor dice: {data}', broadcast=True)




def create_socket(app: Flask) -> SocketIO:
    socketio.init_app(app, logger=True)
    # Registrar el namespace '/chat'
    socketio.on_namespace(ChatNamespace('/chat'))
    return socketio

@app.route('/')
def index():
    return "Servidor Flask con SocketIO y namespace /chat corriendo"

if __name__ == '__main__':
    sio = create_socket(app)
    sio.run(app, debug=True, host='0.0.0.0', port=5000)
