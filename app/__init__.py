import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import DevelopmentConfig
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import config
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os


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

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    configure_uploads(app, avatars)

    if not app.debug or app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(loggin.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/flaskapp.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FlaskApp startup')
    return app

# Evita importaciones recursivas
from app import models
