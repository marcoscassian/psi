from flask import Flask
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)