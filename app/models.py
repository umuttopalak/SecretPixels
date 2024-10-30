import os
from datetime import datetime

from fernet import Fernet
from flask_sqlalchemy import SQLAlchemy

from app import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    secret_key = db.Column(db.String(256), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "secret_key": self.secret_key,
        }

    def create_secret_key(self):
        self.secret_key = Fernet.generate_key()
        db.session.commit()


class TwoFactorAuthModel(db.Model):
    __tablename__ = 'two_factor_auth'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    is_used = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "code": self.code,
            "expires_at": self.expires_at,
            "used_at": self.used_at,
            "is_used": self.is_used,
            "is_active": self.is_active
        }

    def is_valid(self):
        return self.used_at is None and self.expires_at > datetime.utcnow() and not self.is_used and self.is_active

    def mark_as_used(self):
        self.used_at = datetime.utcnow()
        self.is_used = True
        db.session.commit()


class UserPassword(db.Model):
    __tablename__ = 'user_passwords'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hashed_password = db.Column(db.String(256), nullable=True)
    purpose = db.Column(db.String(256), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "hashed_password": self.hashed_password,
            "purpose": self.purpose,
        }
