from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin, UserManager
from sqlalchemy_utils import ChoiceType

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


class Caregivers(db.Model):
    referencesChoice = [('Yes', 'yes'),
                        ('No', 'no'),
                        ('N/A', 'n/a')]
    availabilityChoice = [
        ('Full-Time', 'FT'),
        ('Part_Time', 'PT')
    ]
    __tablename__ = 'caregivers'
    id = db.Column('caregiver_id', db.Integer, primary_key=True)
    experience = db.Column(db.String(100))
    references = db.Column(ChoiceType(referencesChoice))
    availability = db.Column(ChoiceType(availabilityChoice))
    languages_spoken = db.Column(db.String(100))
    background_check = db.Column(db.Boolean)
    additional_notes = db.Column(db.Text)


class CareSeekers(db.Model):
    __tablename__ = 'careSeekers'
    availabilityPreference = [
        ('Full-Time', 'FT'),
        ('Part_Time', 'PT')
    ]
    id = db.Column('careSeeker_id', db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    type_of_care_needed = db.Column(db.String(100))
    monthly_budget = db.Column(db.Integer)
    availability_needed = db.Column(ChoiceType(availabilityPreference))
    preferred_qualifications = db.Column(db.String(100))
    medical_conditions = db.Column(db.String(100))


usermanager = UserManager(None, None, None)
