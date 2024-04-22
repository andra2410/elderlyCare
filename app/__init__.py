from flask import Flask, Blueprint, current_app
from flask_login import LoginManager
from flask_mail import Mail

from .models import db, usermanager, Caregivers, CareSeekers
from .routes import home_blueprint, auth_blueprint
from os import path


def create_app():
    # Get the absolute path of the 'app/templates' directory
    templates_path = path.abspath(path.join(path.dirname(__file__), 'templates'))

    app_flask = Flask(__name__, template_folder=templates_path)
    app_flask.secret_key = '3'
    app_flask.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elderlycare.db'
    app_flask.config['USER_EMAIL_SENDER_EMAIL'] = 'my_flask_app@me.com'
    app_flask.config['MAIL_SERVER'] = '127.0.0.1'
    app_flask.config['MAIL_PORT'] = 1025
    app_flask.config['MAIL_USE_TLS'] = False
    app_flask.config['MAIL_USE_SSL'] = False

    app_flask.register_blueprint(auth_blueprint)
    app_flask.register_blueprint(home_blueprint)

    db.init_app(app_flask)
    with app_flask.app_context():
        usermanager.init_app(app_flask, db, [Caregivers, CareSeekers])
        db.create_all()
    return app_flask
