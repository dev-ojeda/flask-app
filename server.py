from datetime import datetime
from flask import request
from app import create_app
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import eventlet
# from flask_socketio import SocketIO, emit 
app = create_app()
CORS(app)
# app.config['SECRET_KEY'] = 'secret!'
# auth = app.config
sio = SocketIO(app,manage_session=True,async_mode="eventlet", cors_allowed_origins="*", ping_timeout=25, ping_interval=10,namespaces=["/chat"])
# sio = socketio.Server(async_mode="eventlet", cors_allowed_origins="*", ping_timeout=25, ping_interval=10,namespaces=["/chat"])
# wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
# Almacén para las sesiones
sessions = {}
message_queue = []

# Evento de conexión
@sio.on('connect',namespace="/chat")
def connect():
    
    client_id = request.sid
    print(f"Cliente conectado: {client_id}")
    data = {
        "message":"¡Bienvenido!",
        'id': client_id,
        "enviado": f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
    }
    # Almacén para las sesiones
    sessions[client_id] = {'data': data}
    sio.emit('update_session', data ,to=client_id, namespace="/chat")
    sio.emit('server_message', data ,to=client_id, namespace="/chat")

# Evento de desconexión
@sio.on('disconnect',namespace="/chat")
def on_disconnect():
    client_id = request.sid
    if client_id in sessions:
        print(f'Cliente desconectado: {client_id}')
        del sessions[client_id]

# Manejar un evento personalizado
@sio.on("desktop_message")
def handle_receive_message(data):
    message = data.get("message")
    username = data.get("username")
    if message and username:
        # Envía el mensaje a todos los clientes conectados
        sio.emit(
            "receive_message",
            {"username": username, "message": message}
        )

@sio.on('session_updated',namespace="/chat")
def handle_send(data):
    client_id = request.sid
    if client_id in sessions:
        datos = {
            "message":data.get("message"),
            'id': [],
            "enviado": f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
        }   
        message_queue.clear()
        sessions[client_id]['data'].update(datos)
        sio.emit('server_message', datos ,to=client_id,namespace="/chat")
    else:
        sio.emit('server_message', {'message': 'La cola está vacía','id': [],"enviado": f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"}, to=client_id,namespace="/chat")
            

# Manejar un evento personalizado
@sio.event
def send_queue_client():
    client_id = request.sid
    if client_id in sessions:
        current_queue = list(message_queue)
        sessions[client_id]['data'].update(current_queue)
        sio.emit(
            "send_message_client",
            {"username": "WEB", "message": current_queue},to=client_id,namespace="/chat"
        )

@sio.event
def send_queue(data):
    client_id = request.sid
    print(f'Cliente: {client_id}')
    if client_id in sessions:
        datos = {
            "message":"Se ha enviado el ID",
            'id': data,
            "enviado": f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
        }  
        message_queue.append(data)
        sessions[client_id]['data'].update(datos)
        sio.emit('server_message', datos,to=client_id,namespace="/chat")

@sio.on("send_message")
def handle_message(data):
    # Recibe el mensaje desde el cliente y lo retransmite
    message = data.get("message")
    username = data.get("username")
    if message and username:
        # Envía el mensaje a todos los clientes conectados
        sio.emit(
            "web_message",
            {"username": username, "message": message}
        )
        sio.emit(
            "receive_message",
            {"username": username, "message": message}
        )

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app.wsgi_app)
    # sio.run(app, host="0.0.0.0", port=5000, debug=True, log_output=True)