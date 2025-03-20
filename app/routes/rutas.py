import json
import secrets
from dotenv import find_dotenv, load_dotenv, set_key
from datetime import datetime, timedelta, timezone
from flask import (
    Response,
    current_app,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from icecream import ic

from app.config import Config
from app.model.form_validator import FormApp

# from app.model.session_interface import UsernameSession
from email_validator import validate_email
from . import main


load_dotenv()
path_env: str = find_dotenv(".env")
message_queue = []

# def get_queue(self, *a):
#     for value in a:
#         message_queue.put(value)


# Usuarios simulados (puedes reemplazar esto con una base de datos)
# users = {"user1": "password1", "user2": "password2", "admin1": "admin1"}
# Simulación de una base de datos
users = {"user1": "password1", "user2": "password2", "admin": "admin"}
autorizacion = {}


def cargar_empleados() -> list[dict]:
    """
    The function `cargar_empleados` reads data from a JSON file and returns it as a list of
    dictionaries.
    :return: The function `cargar_empleados()` is returning a list of dictionaries containing employee
    data.
    """
    datos = list[dict]
    try:
        with open("resultados.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        ic("Error: El archivo no se encuentra.")
    except json.JSONDecodeError:
        ic("Error: El archivo no tiene un formato JSON válido.")
    finally:
        archivo.close()
    return datos


# Generar un token CSRF y almacenarlo en la sesión
# def generate_csrf_token():
#     if "_csrf_token" not in session:
#         session["_csrf_token"] = secrets.token_hex(16)
#     return session["_csrf_token"]


# Decorador para verificar el token CSRF
# def is_oauth(f):
#     def wrapper(*args, **kwargs):
#         csrf_token = session.get("csrf_token", None)
#         # Leer el token de CSRF desde los datos enviados
#         request_token = request.headers.get("X-CSRFToken")
#         if not csrf_token or csrf_token != request_token:
#             abort(403)  # CSRF Fallido
#         return f(*args, **kwargs)

#     wrapper.__name__ = f.__name__
#     return wrapper


# The `@main.after_request` decorator in Flask is used to register a function that will be called
# after each request made to the Flask application. In this case, the `add_security_headers` function
# is registered as an after-request handler for the `main` blueprint.
# @main.after_request
# def add_security_headers(response: Response) -> Response:
#     """
#     The function `add_security_headers` adds various security-related HTTP headers to a response object
#     in Python.

#     :param response: The function `add_security_headers` takes a `Response` object as input and adds
#     various security headers to it. Here's a breakdown of the security headers being added:
#     :type response: Response
#     :return: The function `add_security_headers` takes a `Response` object as input, adds various
#     security headers to it, and then returns the updated `Response` object with the added security
#     headers.
#     """

#     response.headers["X-Content-Security-Policy"] = (
#         "default-src 'self'; connect-src 'self'; script-src 'self'; img-src 'self'; font-src 'self'; style-src 'self' 'unsafe-inline'; object-src 'none';"
#     )
#     response.headers["X-Frame-Options"] = "DENY"
#     response.headers["X-Content-Type-Options"] = "nosniff"
#     response.headers["X-Referrer-Policy"] = "no-referrer"
#     response.headers["X-Permissions-Policy"] = (
#         "geolocation=(), camera=(), microphone=(), payment=()"
#     )
#     # Opcional: Permitir CORS
#     response.headers["X-Access-Control-Allow-Origin"] = "*"
#     if request.method == "GET" and request.path == "/":
#         response.set_cookie("session", "", expires=0)
#         response.set_cookie("ctx", "", expires=0)
#         response.headers.pop("Set-Cookie", None)
#         return response
#     elif request.method == "GET" and request.path == "/login":
#         response.set_cookie("session", "", expires=0)
#         response.set_cookie("ctx", "", expires=0)
#         response.headers.pop("Set-Cookie", None)
#         return response
#     elif request.method == "POST" and request.path == "/login":
#         response.set_cookie("session", "", expires=0)
#         response.set_cookie("ctx", "", expires=0)
#         response.headers.pop("Set-Cookie", None)
#         response.headers["Cache-Control"] = (
#             "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
#         )
#         response.headers["Pragma"] = "no-cache"
#         response.headers["Expires"] = "0"
#         response.headers["X-CSRFToken"] = session.get("csrf_token", None)
#         return response
#     elif request.method == "GET" and request.path == "/dashboard":
#         response.set_cookie("session", "", expires=0)
#         response.set_cookie("ctx", "", expires=0)
#         response.headers["X-CSRFToken"] = session.get("csrf_token", None)
#         return response
#     elif request.method == "GET" and request.path == "/logout":
#         response.set_cookie("session", "", expires=0)
#         response.set_cookie("ctx", "", expires=0)
#         response.headers.pop("Set-Cookie", None)
#         response.headers["Cache-Control"] = (
#             "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
#         )
#         response.headers["Pragma"] = "no-cache"
#         response.headers["Expires"] = "0"
#         return response
#     else:
#         return response


# The `@login_manager.user_loader` decorator in Flask-Login is used to register a callback function
# that loads a user from the session. This callback function is responsible for reloading a user
# object from the user ID stored in the session.
# Rutas de Flask


# @login_manager.user_loader
# def load_user(username: str) -> User:
#     """
#     The function `load_user` takes a user ID as input and returns a `User` object.

#     :param user_id: The `user_id` parameter is a string that represents the unique identifier of a user.
#     It is used as input to the `load_user` function to load and return a `User` object associated with
#     that specific user ID
#     :type user_id: str
#     :return: An instance of the `User` class with the `user_id` provided as an argument.
#     """
#     ic(username)
#     if "username" in session:
#         username = session.get("username")

#     return User(username)


# The `@main.route("/")` decorator in Flask is defining a route for the URL "/" within the `main`
# blueprint. When a user accesses the root URL of the application (e.g., http://example.com/), the
# function associated with this route will be executed. In this case, the function is redirecting the
# user to the "login" route using `redirect(url_for("main.login"))`.


# @main.before_request
# def verificar_autenticacion():
#     if "username" in session:
#         flash("Por favor, inicia sesión primero", "warning")


@main.before_request
def track_session_start():
    """Guardar el inicio de la sesión si no está ya definido."""
    if "session_start" not in session:
        session["session_start"] = datetime.strftime(
            datetime.now(timezone.utc), "%Y-%m-%d %H:%M:%S.%f"
        )


@main.route("/")
def index() -> Response:
    return redirect(url_for("main.login"))


@main.route("/unauthorized")
def unauthorized() -> Response:
    return make_response(render_template("unauthorized.html"), 401)


# The `@main.route("/login", methods=["GET", "POST"])` decorator in Flask is defining a route for the
# URL "/login" that can handle both GET and POST requests. When a user accesses the "/login" URL with
# a GET request, the `login()` function associated with this route will render the login.html
# template. When a user submits a form on the login page with a POST request, the `login()` function
# will process the form data (username and password), validate the credentials, and handle the login
# logic accordingly.
# @main.route("/login", methods=["GET", "POST"])
# def login() -> Response | str:
#     """
#     The `login()` function in Python handles user authentication by checking credentials and redirecting
#     to the main page upon successful login.
#     :return: The `login()` function returns either a `Response` object or a string. If the request
#     method is "POST" and the credentials are validated successfully, it will redirect to the
#     "main.principal" route with a success message. If the credentials are incorrect, it will flash a
#     danger message. If the request method is not "POST", it will render the "login.html" template.
#     """
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         # Validar credenciales
#         if username in users and users[username] == password:
#             # duration = timedelta(days=0, hours=0, minutes=3, microseconds=0.0)
#             # user = User(username)
#             # login_user(user, remember=False, duration=duration, force=True, fresh=True)
#             session.username = username
#             session["logged_in"] = True  # Almacena el usuario en la sesión
#             user_name_session: UsernameSession = si.open_session(
#                 app=current_app, request=request
#             )
#             ic(user_name_session)
#             response = redirect(url_for("main.dashboard"))
#             # flash("Inicio de sesión exitoso", "success")
#             si.save_session(app=current_app, session=session, response=response)
#             ic(si)
#             return response
#         else:
#             flash("Credenciales incorrectas", "danger")
#     elif request.method == "GET":
#         flash("BIENVENIDO", "success")
#     return render_template(
#         "login.html",
#         hora_actual=f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}",
#     )


# Ruta para manejar eventos del navegador
@main.route("/handle_event", methods=["POST"])
def handle_event():
    data = request.json
    event_type = data.get("event_type")
    details = data.get("details")

    # Procesar los datos según el tipo de evento
    response_message = f"Evento '{event_type}' recibido con detalles: {details}"
    ic(response_message)  # Imprimir en consola del servidor

    return jsonify({"message": response_message})


# The `@main.route("/principal")` decorator in Flask is used to define a route for the specified URL
# ("/principal") that will be handled by the `principal()` function.
# @main.route("/dashboard")
# @is_oauth
# def dashboard() -> Response | str:
#     """
#     The function `principal` checks if the current user is authenticated and redirects to the login page
#     if not, otherwise it renders the principal.html template with user information.
#     :return: The function `principal()` is returning a `Response` object or a string. The specific
#     content of the response or string is not provided in the code snippet.
#     """
#     ic(request.headers)
#     ic(current_app.config)
#     # Datos simulados para el dashboard
#     if "username" in session:
#         flash("Por favor, inicia sesión primero", "warning")
#         return redirect(url_for("main.unauthorized"))
#     elif not session["logged_in"]:
#         flash("Por favor, debe logearse nuevamente", "warning")
#         return redirect(url_for("main.login"))
#     else:
#         return render_template(
#             "dashboard.html",
#             username=session.get("username"),
#             entries=cargar_empleados(),
#         )


@main.route("/login", methods=["GET", "POST"])
def login():
    # In the provided code snippet, the `form` variable is being used to create an instance of the
    # `FormApp` class. This instance is used to process form data submitted in the login route of a
    # Flask application. The `form` variable is initialized as `FormApp()` at the beginning of the
    # `login` route function.
    form = FormApp()
    if request.method == "POST":
        if form.validate_on_submit():
            ValidatedEmail = validate_email(form.email.data)
            ic(ValidatedEmail)
            email = ValidatedEmail.original
            password = form.password.data
            session["user"] = email
            session["password"] = password
            session["session_start"] = datetime.strftime(
                datetime.now(timezone.utc), "%Y-%m-%d %H:%M:%S.%f"
            )
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("main.layout"))
        flash("Por favor, ingresa un nombre de usuario", "danger")
    elif request.method == "GET":
        flash("BIENVENIDO", "success")
    return render_template("login.html", form=form)


@main.route("/layout")
def layout():
    user = session.get("user", "Invitado")
    session_start = session.get("session_start")
    time_left = timedelta
    if session_start:
        session_start = datetime.strptime(session_start, "%Y-%m-%d %H:%M:%S.%f")
        time_elapsed = datetime.now(timezone.utc) - session_start.now(timezone.utc)
        time_left = Config.PERMANENT_SESSION_LIFETIME - time_elapsed
        ic(time_left)
        ic(time_left.total_seconds())
        if time_left.total_seconds() <= 0:
            session.clear()
            flash(
                "Tu sesión ha expirado. Por favor, inicia sesión nuevamente.", "danger"
            )
            return redirect(url_for("main.login"))
    else:
        time_left = timedelta(0)
    return render_template("layout.html", user=user, time_left=time_left)


@main.route("/logout")
def logout():
    session.pop("user", None)  # Eliminar usuario de la sesión
    session.clear()
    flash("Has cerrado sesión", "info")
    return redirect(url_for("main.login"))


@main.before_request
def check_session_timeout():
    now = datetime.now(timezone.utc)
    if "last_activity" in session:
        last_activity = session["last_activity"]
        elapsed_time = now - last_activity
        if elapsed_time > Config.PERMANENT_SESSION_LIFETIME:
            session.clear()  # Limpia la sesión si ha caducado
            flash(
                "Tu sesión ha expirado. Por favor, inicia sesión nuevamente.", "warning"
            )
            return redirect(url_for("main.logout"))
    session["last_activity"] = now


@main.app_errorhandler(404)
def not_found(error) -> Response:
    return make_response(render_template("error.html"), 404)


@main.route("/select-row", methods=["POST"])
def select_row() -> Response:
    row_data = request.get_json()
    row_id: int = row_data.get("id")
    message_queue.append(row_data)
    # Procesar el ID seleccionado
    return jsonify({"message": "Fila seleccionada con éxito", "id": row_id})


# Ruta para generar tokens y secretos
# @main.route("/generate-token", methods=["GET"])
# def generate_token():
#     flash("Se ha generado la autenticacion", "info")
#     return jsonify({"mensaje": "Se ha generado la autenticacion"})


@main.errorhandler(500)
def internal_error(error):
    return "Error interno del servidor", 500


@main.route("/generate-token", methods=["GET"])
def generate_token():
    data: json = request.json  # Recibir datos del cliente
    user_id: str = data.get("user_id")
    token: str = secrets.token_hex(32)  # Genera un token de 32 bytes (hexadecimal)
    secret: str = secrets.token_urlsafe(64)  # Genera un secreto seguro para URLs
    autorizacion["user_id"] = user_id
    autorizacion["token"] = token
    autorizacion["secret"] = secret
    set_env: bool = set_key(path_env, "TOKEN_WEB", autorizacion["token"])
    flash("Se ha generado la autenticacion", "info")
    return jsonify({"mensaje": "Se ha generado la autenticacion", "validate": set_env})
