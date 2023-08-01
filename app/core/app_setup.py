from flask import g, jsonify, Response, request
from main import app
from models.database import db
from controllers import ecg, user as user_controller

app.initialize(db)


@app.route('/ecg/process', methods=['POST'])
@app.auth_required(['user'])
def process_ecg() -> Response:
    """Process ECG Endpoint"""
    data = request.get_json()

    # TODO: Here we should validate incoming data JSON Schema 

    response, code = ecg.process_ecg(data)
    return jsonify(response), code


@app.route('/ecg/<string:ecg_id>', methods=['GET'])
@app.auth_required(['user'])
def check_ecg(ecg_id) -> Response:
    """Get ECG Results"""
    response, code = ecg.get_ecg(ecg_id)
    return jsonify(response), code


@app.route('/token', methods=['POST'])
def req_token() -> Response:
    """Request token endpoint"""
    data = request.get_json()

    # TODO: Here we should validate incoming data JSON Schema 

    user = data.get('user')
    password = data.get('password')

    response, code = user_controller.request_token(user, password)

    return jsonify(response), code


@app.route('/user', methods=['POST'])
@app.auth_required(['admin'])
def create_user() -> Response:
    """Create user endpoint"""
    data = request.get_json()

    # TODO: Here we should validate incoming data JSON Schema 
    username = data.get('user')
    password = data.get('password')
    roles = data.get('roles')

    op_params = {"roles": roles}
    op_params = {k: v for k, v in op_params.items() if v}

    response, code = user_controller.create_user(username, password, **op_params)

    return jsonify(response), code


@app.route('/user/hello', methods=['GET'])
@app.auth_required(['user', 'admin'])
def hello_user() -> Response:
    """Debug method, used to check JWT auth"""
    return f"Hello {g.user.name}"
