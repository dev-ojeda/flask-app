from ast import List
import json
from flask import Response, jsonify, make_response, render_template, request
from icecream import ic
from . import main
message_queue: List = []
# Ruta del archivo JSON
def cargar_empleados() -> list[dict]:
    datos = list[dict]
    try:
        with open('resultados.json', 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
            ic("Error: El archivo no se encuentra.")
    except json.JSONDecodeError:
            ic("Error: El archivo no tiene un formato JSON válido.")
    return datos

# def get_queue(self, *a):
#     for value in a:
#         message_queue.put(value)
@main.after_request
def add_security_headers(response: Response) -> Response:
    response.headers['Content-Security-Policy'] = "default-src 'self';"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@main.route("/")
def index() -> str:
    return render_template("index.html", entries=cargar_empleados())

# @main.route("/")
# def index():
#     return render_template("chat_pro.html")
    
@main.route('/select-row', methods=['POST'])
def select_row() -> Response:
    row_data = request.get_json()
    row_id: int = row_data.get('id')
    message_queue.append(row_data)
    # Procesar el ID seleccionado
    ic(f"ID seleccionado: {row_id}")
    return jsonify({"message": "Fila seleccionada con éxito", "id": row_id})

@main.errorhandler(404)
def not_found(error) -> Response:
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp