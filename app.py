from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import DevConfig
from models import User, Message, ContactList
from exts import db
from events import socketio
from namespaces.auth import auth_ns
from namespaces.user import user_ns
from namespaces.request import request_ns
from namespaces.contact import contact_ns
from namespaces.message import message_ns

def create_app(config_obj=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    api = Api(app, validate=True, doc="/docs") # remove doc on prod

    CORS(app)
    migrate = Migrate(app, db)

    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(request_ns)
    api.add_namespace(contact_ns)
    api.add_namespace(message_ns)

    db.init_app(app)
    JWTManager(app)
    socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "Message": Message,
            "Contact": ContactList
        }
    return app