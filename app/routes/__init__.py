from flask import Blueprint
main = Blueprint('main', __name__,template_folder="templates",static_folder="static",static_url_path="/static")
from . import routes_app, socketio_events