import tkinter as tk
from socketio import Client

# Configurar el cliente Socket.IO
sio = Client()


# Conectar al servidor Flask en el namespace /chat
@sio.on("connect")
def on_connect():
    print("Conectado al namespace /chat")
    update_log("Conectado al servidor")


@sio.on("disconnect")
def on_disconnect():
    print("Desconectado del namespace /chat")
    update_log("Desconectado del servidor")


@sio.on("respuesta", namespace="/chat")
def on_respuesta(data):
    print(f"Respuesta del servidor: {data}")
    update_log(f"Servidor: {data}")


def connect_to_server():
    sio.connect("http://localhost:5000")


def send_message():
    mensaje = entry_message.get()
    if mensaje:
        sio.emit("mensaje", mensaje)
        update_log(f"Tú: {mensaje}")
        entry_message.delete(0, tk.END)


def update_log(message):
    text_log.insert(tk.END, message + "\n")
    text_log.see(tk.END)


# Crear la interfaz Tkinter
root = tk.Tk()
root.title("Chat con Flask-SocketIO")

frame = tk.Frame(root)
frame.pack(pady=10)

text_log = tk.Text(frame, height=15, width=50, state="normal")
text_log.pack()

entry_message = tk.Entry(frame, width=40)
entry_message.pack(side=tk.LEFT, padx=5)

btn_send = tk.Button(frame, text="Enviar", command=send_message)
btn_send.pack(side=tk.LEFT)

# Conectar al servidor al iniciar la aplicación
connect_to_server()

root.protocol("WM_DELETE_WINDOW", lambda: (sio.disconnect(), root.destroy()))
root.mainloop()
