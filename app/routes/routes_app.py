import threading 
from flask import Blueprint, jsonify, make_response, render_template, request
from icecream import ic
# from services.eventos_bus import EmpleadoService, EventEmitter

# event_bus = EventEmitter()
message_queue = []
queue_lock = threading.Lock()
# Crear un Blueprint para modular las rutas
main = Blueprint('main', __name__, template_folder="templates",static_folder="static",static_url_path="/static")

# def cargar_empleados() -> list[dict]:
#     empleado = EmpleadoService(
#         event_bus, "ListarEmpleado", "listar_empleado"
#     )

#     return empleado.listar_empleado()

# def get_queue(self, *a):
#     for value in a:
#         message_queue.put(value)

# @main.route("/")
# def index():
#     return render_template("index.html", entries=cargar_empleados())

@main.route("/")
def index():
    return render_template("chat_pro.html")
    
@main.route('/select-row', methods=['POST'])
def select_row():
    row_data = request.get_json()
    row_id = row_data.get('id')
    message_queue.append(row_data)
    # Procesar el ID seleccionado
    ic(f"ID seleccionado: {row_id}")
    return jsonify({"message": "Fila seleccionada con éxito", "id": row_id})

@main.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp