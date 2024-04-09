from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType

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
    referencesChoice = [('Yes', 'yes'),
                        ('No', 'no'),
                        ('N/A', 'n/a')]
    availabilityChoice = [
        ('Full-Time', 'FT'),
        ('Part_Time', 'PT')
    ]
    # !!!Yes is the one displayed, while yes is the value stored in the db
    __tablename__ = 'caregivers'
    id = db.Column('caregiver_id',db.Integer, primary_key=True)
    experience = db.Column(db.String(100))
    references = db.Column(ChoiceType(referencesChoice))
    availability = db.Column(ChoiceType(availabilityChoice))
    languages_spoken = db.Column(db.String(100))
    background_check = db.Column(db.Boolean)
    additional_notes = db.Column(db.Text)


class CareSeekers(Users):
    __tablename__ = 'careSeekers'
    availabilityPreference = [
        ('Full-Time', 'FT'),
        ('Part_Time', 'PT')
    ]
    id = db.Column('careSeeker_id',db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    type_of_care_needed = db.Column(db.String(100))
    monthly_budget = db.Column(db.Integer)
    availability_needed = db.Column(ChoiceType(availabilityPreference))
    preferred_qualifications = db.Column(db.String(100))
    medical_conditions = db.Column(db.String(100))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
