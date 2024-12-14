import queue
from flask import Flask, redirect, render_template, request, jsonify, url_for

# from flask_socketio import SocketIO, emit
from flask_socketio import SocketIO, emit
from services.eventos_bus import EmpleadoService, EventEmitter


class WebApp:

    def __init__(self, name):
        # Crear la instancia de Flask
        self.app = Flask(name)
        self.sio = SocketIO(self.app, cors_allowed_origins="*", ping_timeout=20, ping_interval=10)
        # self.sio = socketio.Server(cors_allowed_origins="*")
        # self.wsgi_app = socketio.WSGIApp(self.socketIO, self.app.wsgi_app)
        # Almacén para manejar sesiones activas
        self.connected_clients = {}
        self.event_bus = EventEmitter()
        self.message_queue = queue.Queue(maxsize=0)
        # Configuración opcional (por ejemplo, claves secretas o configuraciones)
        self.app.config["SECRET_KEY"] = "clavesecreta"
        # Registrar las rutas
        self._register_routes()

    def cargar_empleados(self) -> list[dict]:
        self.empleado = EmpleadoService(
            self.event_bus, "ListarEmpleado", "listar_empleado"
        )

        return self.empleado.listar_empleado()

    def queue(self, *a):
        for value in a:
            self.message_queue.put(value)


    def _register_routes(self):
        """Método para definir las rutas de la aplicación."""

        @self.app.route("/")
        def home():
            return render_template("index.html", entries=self.cargar_empleados())

        @self.app.route("/api/data", methods=["GET"])
        def api_data():
            return jsonify({"message": "¡Hola, Flask!", "status": "success"})

        # Ruta para mostrar el formulario
        @self.app.route("/form", methods=["GET", "POST"])
        def form():
            if request.method == "POST":
                # Obtener los datos enviados desde el formulario
                name = request.form.get("name")
                email = request.form.get("email")
                message = request.form.get("message")

                # Aquí podrías procesar o almacenar los datos, por ejemplo, en una base de datos
                print(f"Nombre: {name}, Email: {email}, Mensaje: {message}")

                # Redirigir a otra página (opcional)
                return redirect(url_for("thanks"))

            # Renderizar el formulario en caso de una solicitud GET
            return render_template("form.html")

        # Ruta para eliminar una entrada
        @self.app.route("/delete/<entry>", methods=["GET", "POST"])
        def delete(entry):
            if request.method == "POST":
                # Obtener los datos enviados desde el formulario
                self.message_queue.put(request.view_args.get("entry"))
                message = self.message_queue.get()
                print(message)
                # Redirigir a otra página (opcional)
                return redirect(
                    url_for("home"),
                    302,
                    jsonify(
                        {
                            "status": "success"
                        }
                    ),
                )
            elif request.method == "GET":
                message = self.message_queue.get()
                print(message)
                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": message,
                        }
                    )
                )
            else:
                return render_template("index.html")
            # empleado.eliminar_empleado()
            # Redirigir a otra página (opcional)

        # Renderizar el formulario en caso de una solicitud GET

        @self.app.route("/form", methods=["POST"])
        def form_handler():
            data = request.form
            return jsonify({"data": data, "message": "Formulario recibido."})

        @self.app.route("/produce", methods=["GET", "POST"])
        def produce():
            """Endpoint para produzir mensagens."""
            # Adiciona a mensagem na fila
            if request.method == "POST":
                data = request.get_json(force=True)
                message = data["message"]
                self.message_queue.put(message)
                return (
                    jsonify({"status": "Mensagem adicionada", "message": message}),
                    200,
                )
            elif request.method == "GET":
                message = {"message": self.message_queue.get()}
                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": message,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Mensagem não fornecida"}), 400

        @self.app.route("/consume", methods=["GET", "POST"])
        def consume():
            """Endpoint para produzir mensagens."""
            if request.method == "POST":
                data = request.get_json(force=True)
                print(data)
                response_data = {}
                response_data["message_received"] = "Recibdo con exito"
                # self.message_queue.put(message)
                return (
                    jsonify(
                        {
                            "status": "Message received",
                            "message": response_data["message_received"],
                        }
                    ),
                    200,
                )
            elif request.method == "GET":
                message = {"message": self.message_queue.get()}
                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": message,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Mensagem não fornecida"}), 400

        # Ruta de agradecimiento
        @self.app.route("/thanks")
        def thanks():
            return "<h1>¡Gracias por enviar el formulario!</h1>"

        @self.sio.on("cliente_message")
        def handle_receive_message(data):
            message = data.get("message")
            username = data.get("username")
            if message and username:
                # Envía el mensaje a todos los clientes conectados
                emit(
                    "receive_message",
                    {"username": username, "message": message},
                    broadcast=True,
                )
            # print(f"Mensaje recibido: {data}")
            # emit("response", f"Servidor recibió: {data}", broadcast=True)

        @self.sio.on("send_message")
        def handle_message(data):
            # Recibe el mensaje desde el cliente y lo retransmite
            message = data.get("message")
            username = data.get("username")
            if message and username:
                # Envía el mensaje a todos los clientes conectados
                emit(
                    "server_message",
                    {"username": username, "message": message},
                    broadcast=True,
                )
                emit(
                    "receive_message",
                    {"username": username, "message": message},
                    broadcast=True,
                )

        # Manejador de conexión
        # @self.socketIO.on("connect")
        # def handle_connect():
        #     print("Cliente conectado")
        #     self.socketIO.emit(
        #         "server_message",
        #         {
        #             "username": "CLIENTE",
        #             "message": "conexion establecida con el cliente",
        #         },
        #     )

        # Manejo de eventos personalizados
        # @self.sio.event
        # def custom_pull(sid, data):
        #     print(f"Cliente {sid} envió: {data}")
        #     response = {"response": f"Hola {data.get('nombre', 'desconocido')}!"}
        #     self.sio.emit("server_message", response, to=sid)

        # # Manejo de desconexión
        # @self.sio.event
        # def disconnect(sid):
        #     print(f"Cliente desconectado: {sid}")

    def main(self):
        """Método para ejecutar la aplicación."""
        # eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), self.wsgi_app)
        # eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), self.app.wsgi_app)
        self.sio.run(self.app, debug=True, host="0.0.0.0", port=5000, log_output=True)
        # self.app.run(host=host, port=port, debug=debug)


# Crear la app y ejecutarla
if __name__ == "__main__":
    app = WebApp(__name__)
    app.main()
