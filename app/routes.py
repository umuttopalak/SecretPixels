import datetime

import jwt
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, request

from .models import UserModel, UserPassword
from .utils import (create_response, generate_2fa_code, send_2fa_email,
                    token_required, verify_2fa_code)


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/health')
def health_check():
    return "OK"


@app.route('/api/authentication/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(
        data['password'], method='pbkdf2:sha256')
    new_user = UserModel(
        name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return create_response(message="User registered successfully!", status=201)


@app.route('/api/authentication/login', methods=['POST'])
def login():
    data = request.get_json()
    user = UserModel.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return create_response(message="Invalid credentials!", status=401)

    code = generate_2fa_code(user.id)
    send_2fa_email(user.email, code)

    return create_response(message="2FA code sent to your email.", status=200)


@app.route('/api/authentication/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.get_json()
    user = UserModel.query.filter_by(email=data['email']).first()
    if not user:
        return create_response(message="User not found!", status=404)

    if verify_2fa_code(user.id, data['code']):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
        return create_response(data={'token': token}, message="2FA verified successfully!", status=200)
    else:
        return create_response(message="Invalid or expired 2FA code!", status=401)


@app.route('/api/user/profile', methods=['GET'])
@token_required
def profile(current_user):
    return create_response(data={"name": current_user.name, "email": current_user.email}, message="User profile fetched successfully!", status=200)


@app.route('/api/user/passwords', methods=['GET'])
@token_required
def list_passwords(current_user):
    passwords = UserPassword.query.filter_by(id=current_user.id).all()
    return create_response(data={"passwords": [password.to_dict() for password in passwords]}, message="User Passwords Retrieved Successfully.")
