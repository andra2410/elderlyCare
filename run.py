from flask import Flask, render_template
from app import create_app
from app.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elderlycare.db'
db.init_app(app)

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        app.run(debug=True)