from flask import Flask
from config import DevelopmentConfig
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import config
from flask_uploads import UploadSet, IMAGES, configure_uploads


bootstrap = Bootstrap()
mail = Mail()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
db = SQLAlchemy()
migrate = Migrate()
avatars = UploadSet('avatars', IMAGES)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    configure_uploads(app, avatars)

    return app

# Evita importaciones recursivas
from app import models
