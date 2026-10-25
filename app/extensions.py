from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_compress import Compress

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
compress = Compress()