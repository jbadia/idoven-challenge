#! /usr/bin/env python3

from pprint import pprint
from main import app
from models.database import db
from core.errors import CreateUserException
from controllers import user as user_controller

# app.initialize(db)

if __name__ == '__main__':
    try:
        response, _ = user_controller.create_default_admin_user()
        pprint(response)
    except CreateUserException:
        print("User already exists")
