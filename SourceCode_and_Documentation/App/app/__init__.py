from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jsglue import JSGlue
from config import Config

# Extension Initialisation
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
jsglue = JSGlue()

# Factory Function
def create_app():
    # Create Flask Instance
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    # Apply Extension to Flask Instance
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    jsglue.init_app(app)

    # Attach routes Blueprints to app
    from .blueprints.main import main
    app.register_blueprint(main)

    from .blueprints.auth import auth
    app.register_blueprint(auth)

    return app
