import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)




def create_app():
    """Application factory pattern for creating Flask app"""
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')

    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///scriptscope.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}

    db.init_app(app)

    # All model and blueprint imports/registrations must be inside app context
    with app.app_context():
        from . import models
        db.create_all()
        from . import routes
        app.register_blueprint(routes.routes_bp)

    return app

# Create app instance for production use
app = create_app()