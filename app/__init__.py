from flask import Flask, request
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)

from app import models, routes
