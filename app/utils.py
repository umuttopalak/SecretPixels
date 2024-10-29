import datetime
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

import cv2
import jwt
import numpy as np
import qrcode
from cryptography.fernet import Fernet
from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from PIL import Image

from app import app, db, mail

from .models import TwoFactorAuthModel, UserModel

key = Fernet.generate_key()
cipher_suite = Fernet(key)
with open('secret.key', 'wb') as key_file:
    key_file.write(key)


def create_response(data=None, message=None, options=None, status=200):
    response = {
        "data": data,
        "message": message,
        "options": options
    }
    return jsonify(response), status


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
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
