from flask import Blueprint

# Generate Blueprint for authentication components of the application
auth = Blueprint('auth', __name__)

from . import routes
