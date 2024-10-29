import os
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from app import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


class TwoFactorAuthModel(db.Model):
    __tablename__ = 'two_factor_auth'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    is_used = db.Column(db.Boolean, nullable=False, default=False)
    
    def is_valid(self):
        return self.used_at is None and self.expires_at > datetime.utcnow()
    
    def mark_as_used(self):
        self.used_at = datetime.utcnow()
        self.is_used = True
        db.session.commit()

