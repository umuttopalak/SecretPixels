# SecretPixels

SecretPixels is a web application that provides secure login, registration, and two-factor authentication (2FA) features for users. It also includes functionality to hash passwords and convert them into images or QR codes for enhanced security.

## Getting Started

This section provides instructions on how to set up and run the project locally.

### Prerequisites

- Python 3.8+
- Flask
- Flask-Mail
- OpenCV
- Pillow
- NumPy
- PyJWT
- Cryptography

### Installation

To set up the project locally, follow these steps:

```bash
git clone https://yourproject.git
cd yourproject
pip install -r requirements.txt
```

### Running the Application

You can run the application with the following command:

```bash
python run.py
```

## Features

### User Registration

New users can register with their name, email, and password. Passwords are securely hashed using the PBKDF2 algorithm.

### User Login

Users can log in using their email and password. After password verification, a 2FA code is sent to their email for added security.

### Two-Factor Authentication (2FA)

Users need to verify their login by entering the 2FA code they received via email.

### Password Conversion to Image and QR Code

User passwords can be converted into an image or QR code and saved to a specified output file. This feature can be used to create visual representations of passwords.

## Development

When working on the project, it is recommended to create a separate branch for each new feature or fix.

## Contributing

If you want to contribute to this project, please follow the contribution guidelines and make a pull request.

## License

This project is licensed under the [MIT License](LICENSE).