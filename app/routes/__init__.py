# `from flask import Blueprint` is importing the `Blueprint` class from the Flask module. This class
# is used to create modular and reusable components in a Flask application.
from flask import Blueprint

# This line of code is creating a Flask Blueprint named 'main' with the specified parameters. Here's a
# breakdown of the parameters:
main = Blueprint(
    "main",
    __name__,
    static_folder="static",
    static_url_path="/static",
    template_folder="templates",
)
# The line `from . import eventos, inicio, rutas` is importing modules named `eventos`, `inicio`, and
# `rutas` from the current package or directory. This allows the code in the current module to access
# functions, classes, or variables defined in those imported modules.
from . import rutas
