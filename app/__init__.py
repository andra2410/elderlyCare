import os

from flask import Flask, Blueprint
from flask_login import LoginManager
from .models import db, usermanager, Users
from .routes import home_blueprint, auth_blueprint
from os import path

login_manager = LoginManager()


def create_app():
    # Get the absolute path of the 'app/templates' directory
    templates_path = path.abspath(path.join(path.dirname(__file__), 'templates'))

    app_flask = Flask(__name__, template_folder=templates_path)
    login_manager.init_app(app_flask)

    app_flask.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    app_flask.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elderlycare.db'
    app_flask.config['USER_EMAIL_SENDER_EMAIL'] = 'my_flask_app@me.com'
    app_flask.config['MAIL_SERVER'] = '127.0.0.1'
    app_flask.config['MAIL_PORT'] = 1025
    app_flask.config['MAIL_USE_TLS'] = False
    app_flask.config['MAIL_USE_SSL'] = False
    app_flask.config['USER_LOGIN_URL'] = '/login'
    app_flask.config['LOGIN_VIEW'] = 'auth.custom_login'
    app_flask.config['LOGIN_MESSAGE'] = 'Please log in to access this page'
    app_flask.config['TESTING'] = True
    app_flask.config['SESSION_COOKIE_SECURE'] = True

    app_flask.register_blueprint(auth_blueprint)
    app_flask.register_blueprint(home_blueprint)

    db.init_app(app_flask)
    # login_manager.login_view = 'auth.custom_login'
    # login_manager.login_message = 'Please log in to access this page'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    with app_flask.app_context():
        usermanager.init_app(app_flask, db, Users)
        db.create_all()
    return app_flask
