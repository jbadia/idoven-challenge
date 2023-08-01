import os
from typing import Callable, Any
from functools import wraps
from datetime import timedelta
from flask import Flask as BaseFlask, Config as BaseConfig, jsonify, g
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request, get_jwt
from redis import Redis
from rq import Queue
from core.errors import GenericError, UnauthorizedError, UnprivilegedError
from models.database import db_session, User


class Config(BaseConfig):
    """Custom config loader"""

    @staticmethod
    def hardcoded() -> dict[str, Any]:
        return {
            "JWT_SECRET_KEY" : 'top secret!',
            "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=1),
            "DATABASE": {
                "provider": "mysql",
                "user": "user",
                "password": "user_password",
                "host": "db",
                "database": "database",
            },
        }

    @staticmethod
    def environment() -> dict[str, Any]:
        return {
            "JWT_SECRET_KEY": os.environ.get("SECRET_KEY", "top secret!"),
            "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=1),
            "DATABASE": {
                "provider": os.environ.get("DATABASE_PROVIDER", "mysql"),
                "user": os.environ.get("DATABASE_USER", "user"),
                "password": os.environ.get("DATABASE_PASSWORD", "user_password"),
                "host": os.environ.get("DATABASE_HOST", "db"),
                "database": os.environ.get("DATABASE_DATABASE", "database"),
            },
        }

    def load_config(self, method: str) -> None:
        for key, val in getattr(self, method)().items():
            self[key] = val


class Flask(BaseFlask):
    """Custom Flask with database initialization and env config"""

    def __init__(self, import_name: str, conf_method: str = "hardcoded", *args, **kwargs):
        super(Flask, self).__init__(import_name, *args, **kwargs)
        self.conf_method = conf_method
        self.db = None

        self.cache = Redis(host='redis', port=6379)
        self.queue = Queue(connection=self.cache)

        self.register_error_handler(GenericError, self.handle_error)

    def initialize(self, db) -> None:
        """method used to load the config and connect with the database"""
        self.config.load_config(self.conf_method)
        db.bind(**self.config["DATABASE"])
        db.generate_mapping(create_tables=True)

        self.jwt = JWTManager(self)

    def make_config(self, instance_relative: bool = False) -> Config:
        """Flask make config overrided"""
        root_path = self.instance_path if instance_relative else self.root_path
        return Config(root_path, self.default_config)

    def disconnect(self) -> None:
        """disconnects database"""
        self.db.disconnect()
    
    def handle_error(self, error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @staticmethod
    def auth_required(roles: list[str] = []) -> Callable:
        """JWT Auth decorator, roles required"""
        def wrapper(fn):
            @wraps(fn)
            @db_session
            def decorator(*args, **kwargs):
                g.user = None
                try:
                    verify_jwt_in_request()
                    claims = get_jwt()
                except Exception as e:
                    print(e)
                    raise UnauthorizedError()

                g.user = User.get(name=get_jwt_identity())

                if g.user is None:
                    raise UnauthorizedError()

                if not set(claims.get("roles", [])).intersection(roles):
                    raise UnprivilegedError()
                return fn(*args, **kwargs)

            return decorator

        return wrapper
    
