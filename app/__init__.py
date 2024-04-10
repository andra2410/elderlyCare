from flask import Flask
from models import db, usermanager, Users, Caregivers, CareSeekers
from routes import auth_blueprint, home_blueprint
from os import path


def create_app():
    templates_path = path.abspath('app/templates')
    instance_path = path.abspath('instance')
    app_flask = Flask(__name__, template_folder=templates_path, instance_path=instance_path)
    app_flask.secret_key = 'my_secret_key'
    app_flask.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elderlycare.db'

    # DEFINE AND CONFIG SMTP SERVER
    app_flask.config['USER_EMAIL_SENDER_EMAIL'] = 'elderlycare@me.com'
    app_flask.config['MAIL_SERVER'] = '126.0.0.1'
    app_flask.config['MAIL_PORT'] = 1025
    app_flask.config['MAIL_USE_TLS'] = False
    app_flask.config['MAIL_USE_SSL'] = False

    # regiser blueprints
    app_flask.register_blueprint(auth_blueprint)
    app_flask.register_blueprint(home_blueprint)

    db.init_app(app_flask)
    with app_flask.app_context():
        usermanager.init_app(app_flask, db, Users)
        db.create_all()
    return app_flask


app = create_app()
