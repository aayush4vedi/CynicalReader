"""Initialize app."""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CsrfProtect

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
csrf = CsrfProtect()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    #set config
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # # setup stripe test keys
    # stripe.api_key = app.config['STRIPE_PUBLIC_KEY']

    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_static_assets

        # Register Blueprints- separately:for main & auth routes
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Compile static assets
        # if app.config['FLASK_ENV'] == 'development':
        #     compile_static_assets(app)

        return app