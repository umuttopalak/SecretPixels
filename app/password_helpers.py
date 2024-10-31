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

cipher_suite = Fernet()


def matrix_to_image(matrix, output_file='output.png', colormap=None):
    if np.issubdtype(matrix.dtype, np.floating):
        matrix = (matrix - np.min(matrix)) / \
            (np.max(matrix) - np.min(matrix)) * 255

    matrix = matrix.astype(np.uint8)

    if colormap:
        matrix = cv2.applyColorMap(matrix, colormap)

    if len(matrix.shape) == 2:
        image = Image.fromarray(matrix, 'L')  # Gri tonlamalı görüntü
    elif len(matrix.shape) == 3 and matrix.shape[2] == 3:
        image = Image.fromarray(matrix, 'RGB')  # Renkli görüntü
    else:
        raise ValueError(
            "Matris boyutları görüntü oluşturmak için uygun değil")

    image.save(output_file)
    print(f"Görüntü '{output_file}' dosyasına kaydedildi.")


def password_to_image(password, output_file='password_image.png', encrypted=False):
    if encrypted:
        password = cipher_suite.encrypt(password.encode()).decode()

    ascii_values = [ord(char) for char in password]

    width = len(ascii_values) * 3
    height = 100
    matrix = np.zeros((height, width, 3), dtype=np.uint8)

    for i, value in enumerate(ascii_values):
        matrix[:, i*3:(i+1)*3] = value % 256

    matrix_to_image(matrix, output_file)


def password_to_qr(password, output_file='password_qr.png', encrypted=False):
    if encrypted:
        password = cipher_suite.encrypt(password.encode()).decode()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(password)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    print(f"QR kod '{output_file}' dosyasına kaydedildi.")


def decode_image_to_password(image_file, encrypted=False):
    image = Image.open(image_file)
    matrix = np.array(image)

    ascii_values = matrix[0, ::3, 0]
    password = ''.join([chr(value) for value in ascii_values if value != 0])

    if encrypted:
        password = cipher_suite.decrypt(password.encode()).decode()

    print(f"Çözümlenen şifre: {password}")
    return password


