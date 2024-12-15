import os
from dotenv import load_dotenv
from flask import request
from icecream import ic
from flask_socketio import SocketIO, emit, Namespace
from app import create_app
load_dotenv()
app = create_app()
socketio = SocketIO(app)
# Diccionario para mantener los usuarios y mensajes
sessions = {}
# Namespace por defecto ('/')
@socketio.on('connect')
def handle_connect():
    ic("Cliente conectado al namespace por defecto")
    emit(
        "message", {"data": "¡Bienvenido al servidor!"}
    )  # Enviar mensaje al cliente conectado
    
@socketio.on('disconnect')
def handle_disconnect():
    ic("Cliente desconectado del namespace por defecto")

# Evento personalizado
@socketio.on("mi_evento")
def handle_mi_evento(data):
    ic("Mensaje recibido al namespace por defecto")
    # Responder al cliente
    emit("respuesta", {"data": f"Recibido tu mensaje: {data['mensaje']}"})

def main():
    ic("Servidor Socket.IO ejecutándose en http://localhost:5000")
    socketio.run(app, debug=False, host=os.getenv("HOST"), port=os.getenv("PORT"), log_output=False,use_reloader=False)
    # eventlet.wsgi.server(eventlet.listen(("localhost", 5000)), app.wsgi_app)
    
# Namespace personalizado ('/chat')
class ChatNamespace(Namespace):
    def on_connect(self):
        client_id = request.sid
        sessions[client_id] = {'data': {}}
        ic(f"Cliente conectado al namespace /chat: {client_id}")
        
    def on_disconnect(self):
        ic("Cliente desconectado del namespace /chat")
        client_id = request.sid
        if client_id in sessions:
            print(f'Cliente desconectado: {client_id}')
            del sessions[client_id]
            
    def on_mensaje(self, data):
        client_id = request.sid
        ic("client_id", client_id)
        chat_mensaje = {
            "username":data['username'],
            "msg":data['msg']
        }
        if client_id in sessions:
            # Almacén para las sesiones
            sessions[client_id]['data'].update(chat_mensaje)
            emit('respuesta', {'mensaje': f"{data['username']}:{data['msg']}"}, broadcast=True)

    # Escuchar eventos personalizados
    def on_client_message(data):
        client_id = request.sid
        ic("client_id", client_id)
        chat_mensaje = {
            "username":data['username'],
            "msg":data['msg'],
        }   
        if client_id in sessions:
            ic("SESSION: ", sessions[client_id]['data']["username"])
            sessions[client_id]['data'].update(chat_mensaje)
            socketio.emit('message_cliente', chat_mensaje, namespace="/chat")
            
    # Crea un evento. para enviar mensajes al cliente.
    socketio.on_event("message_cliente",on_client_message, namespace="/chat")

    # Escuchar eventos personalizados
    # def on_receive_message(data):
    #     client_id = request.sid
    #     ic("client_id", client_id)
    #     chat_mensaje = {
    #         "username":data['username'],
    #         "msg":data['msg']
    #     }
    #     if client_id in sessions:
    #         ic("SESSION: ", sessions[client_id]['data']["username"])
    #         sessions[client_id]['data'].update(chat_mensaje)
    #         ic(f"Mensaje recibido: {chat_mensaje}")
    # # Crea un evento. para mensajes mensajes del cliente DESKTOP.
    # socketio.on_event("message",on_receive_message, namespace="/chat")


# Registrar el namespace personalizado
socketio.on_namespace(ChatNamespace('/chat'))

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    main()