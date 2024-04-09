from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elderlycare.db'
db = SQLAlchemy(app)


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


class Users(db.Model):
    __abstract__ = True
    # id = db.Column('caregiver_id', db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


class Caregivers(Users):
    pass


if __name__ == '__main__':
    app.run(debug=True)
