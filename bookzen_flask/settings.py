import os

MONGODB_SETTINGS = {
        'db': 'bookzen',
        'host': 'mongodb://localhost:27017/'}

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY", "Ringa Linga")

MY_EMAIL_ADDRESS = "youremail@gmail.com"
EMAIL_ACCOUNT = "Gmailaccount"
EMAIL_PASSWORD = "Gmailpass"

INSTAGRAM_USER = ""
INSTAGRAM_PASSWORD = ""
