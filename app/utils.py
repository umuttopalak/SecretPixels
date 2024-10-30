import datetime
import random
from functools import wraps

import jwt
from flask import jsonify, request
from flask_mail import Message

from app import app, db, mail

from .models import TwoFactorAuthModel, UserModel


def create_response(data=None, message=None, options=None, status=200):
    response = {
        "status": status,
        "data": data,
        "message": message,
        "options": options
    }
    return jsonify(response), status


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = UserModel.query.filter_by(
                id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


def send_2fa_email(to_email, code):
    try:
        msg = Message(
            subject="Authentication Key",
            sender=str(app.config.get("MAIL_DEFAULT_SENDER")),
            recipients=[to_email],
            html=app.config.get("AUTH_MAIL_HTML").format(to_email, code)
        )
        mail.send(msg)
    except Exception as e:
        print(str(e))

    print(f"2FA email sent to {to_email}")


def generate_2fa_code(user_id):
    code = f"{random.randint(100000, 999999)}"
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
    two_factor_auth = TwoFactorAuthModel(
        user_id=user_id, code=code, expires_at=expires_at)
    db.session.add(two_factor_auth)
    db.session.commit()
    return code


def verify_2fa_code(user_id, code):
    two_factor_auth = TwoFactorAuthModel.query.filter_by(
        user_id=user_id, code=code).first()
    if two_factor_auth.is_valid():
        two_factor_auth.mark_as_used()
        return True
    return False


def resend_2fa_code(user_id):
    try:
        old_codes = TwoFactorAuthModel.query.filter_by(
            user_id=user_id, is_used=False).all()
        for code in old_codes:
            code.is_used = False
            code.is_active = False
            code.used_at = datetime.utcnow()
        db.session.commit()

        new_code = generate_2fa_code(user_id)
        user_email = UserModel.query.filter_by(id=user_id).first().email
        send_2fa_email(user_email, new_code)
        return True
    except Exception as e:
        print(str(e))
        return False
