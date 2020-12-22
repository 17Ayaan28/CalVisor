from flask import Blueprint

# Generate Blueprints for main components of the application
main = Blueprint('main', __name__)

from . import routes
