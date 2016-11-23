import os

MONGODB_SETTINGS = {
        'db': 'bookzen',
        'host': 'mongodb://localhost:27017/'}

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY", "Ringa Linga")

MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "")
EMAIL_ACCOUNT = os.environ.get("EMAIL_ACCOUNT", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
