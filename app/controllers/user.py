from typing import Any
from flask_jwt_extended import create_access_token
from core.errors import UnauthorizedError, CreateUserException
from models.database import db_session, User, flush

@db_session
def request_token(user: str, password: str) -> tuple[dict, str]:
    user = User.get(name=user)

    if not user or not user.verify_password(password):
        raise UnauthorizedError()
    
    access_token = create_access_token(user.name, additional_claims={"roles": user.roles})
    return {"access_token": access_token}, 200


@db_session
def create_user(username: str, password: str, roles: list[str] = ['user']) -> tuple[dict, str]:
    user = User.get(name=username)

    if user:
        raise CreateUserException(message="User already exists")
    
    user = User(name=username, password=password, roles=roles)

    flush()

    response = {
        "id": user.id,
        "name": user.name,
        "roles": user.roles,
    }
    
    return response, 201


def create_default_admin_user():
    create_user("admin", "admin", ["admin"])