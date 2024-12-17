from ast import Dict
from flask import request
from flask_socketio import Namespace
from dotenv import load_dotenv
from icecream import ic
from .. import socketio  # Importar la instancia global de SocketIO
load_dotenv()
# Diccionario para mantener los usuarios y mensajes
sessions: Dict = {}
# Namespace por defecto ('/')
@socketio.on('connect')
def handle_connect() -> None:
    """
        Funcion que realiza la conexion de un namespace por defecto
    """
    ic("Cliente conectado al namespace por defecto")
    socketio.emit(
        "message", {"data": "¡Bienvenido al servidor!"}
    )  # Enviar mensaje al cliente conectado
    
@socketio.on('disconnect')
def handle_disconnect() -> None:
    """
        Funcion que realiza la desconexion de un namespace por defecto
    """
    ic("Cliente desconectado del namespace por defecto")

# Evento personalizado
@socketio.on("mi_evento")
def handle_mi_evento(data) -> None:
    """
    Crea un evento para ser invocado en un namespace por defecto
    Args:
        data (json): Datos que envia del mensaje de un receptor 
    """
    ic("Mensaje recibido al namespace por defecto")
    # Responder al cliente
    socketio.emit("respuesta", {"data": f"Recibido tu mensaje: {data['mensaje']}"})

# Namespace personalizado ('/chat')
class ChatNamespace(Namespace):
    def on_connect(self) -> None:
        client_id: str = request.sid
        sessions[client_id] = {'data': {}}
        ic(f"Cliente conectado al namespace /chat: {client_id}")
        
    def on_disconnect(self) -> None:
        ic("Cliente desconectado del namespace /chat")
        client_id: str = request.sid
        
        if client_id in sessions:
            chat_mensaje = {
                "username":sessions[client_id]['data']["username"],
                "msg":"Cliente desconectado"
            }
            ic(f'Cliente desconectado: {chat_mensaje["username"]}')
            ic(f'Cliente desconectado: {client_id}')
            socketio.emit('respuesta', chat_mensaje, namespace="/chat")
            del sessions[client_id]
            
    def on_mensaje(self, data) -> None:
        client_id: str = request.sid
        ic("client_id", client_id)
        ic("username", data['username'])
        ic("msg", data['msg'])
        chat_mensaje = {
            "username":data['username'],
            "msg":data['msg']
        }
        if client_id in sessions:
            # Almacén para las sesiones
            ic("chat_mensaje", chat_mensaje)
            sessions[client_id]['data'].update(chat_mensaje)
            socketio.emit('respuesta', chat_mensaje, namespace="/chat")

    # Escuchar eventos personalizados
    def on_client_message(data) -> None:
        client_id: str = request.sid
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

# Namespace personalizado ('/chat')
class QueueNamespace(Namespace):
    def on_connect(self) -> None:
        client_id: str = request.sid
        sessions[client_id] = {'data': {}}
        ic(f"Cliente conectado al namespace /chat: {client_id}")
        
    def on_disconnect(self) -> None:
        ic("Cliente desconectado del namespace /chat")
        client_id: str = request.sid
        
        if client_id in sessions:
            chat_mensaje = {
                "username":sessions[client_id]['data']["username"],
                "msg":"Cliente desconectado"
            }
            ic(f'Cliente desconectado: {chat_mensaje["username"]}')
            ic(f'Cliente desconectado: {client_id}')
            socketio.emit('respuesta', chat_mensaje, namespace="/chat")
            del sessions[client_id]
            
    def on_mensaje(self, data) -> None:
        client_id: str = request.sid
        ic("client_id", client_id)
        ic("username", data['username'])
        ic("msg", data['msg'])
        chat_mensaje = {
            "username":data['username'],
            "msg":data['msg']
        }
        if client_id in sessions:
            # Almacén para las sesiones
            ic("chat_mensaje", chat_mensaje)
            sessions[client_id]['data'].update(chat_mensaje)
            socketio.emit('respuesta', chat_mensaje, namespace="/chat")

    # Escuchar eventos personalizados
    def on_client_message(data) -> None:
        client_id: str = request.sid
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



# Registrar el namespace personalizado
socketio.on_namespace(ChatNamespace('/chat'))
socketio.on_namespace(ChatNamespace('/queue'))
