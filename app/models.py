from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin, UserManager
from sqlalchemy_utils import ChoiceType

db = SQLAlchemy()


class Caregivers(db.Model, UserMixin):
    __tablename__ = 'caregivers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer)
    experience = db.Column(db.String(100))
    references = db.Column(ChoiceType([('Yes', 'yes'), ('No', 'no'), ('N/A', 'n/a')]))
    availability = db.Column(ChoiceType([('Full-Time', 'FT'), ('Part-Time', 'PT')]))
    languages_spoken = db.Column(db.String(100))
    background_check = db.Column(db.Boolean)
    additional_notes = db.Column(db.Text)

    def is_active(self):
        return self.is_enabled


class CareSeekers(db.Model, UserMixin):
    __tablename__ = 'care_seekers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    type_of_care_needed = db.Column(db.String(100))
    monthly_budget = db.Column(db.Integer)
    availability_needed = db.Column(ChoiceType([('Full-Time', 'FT'), ('Part-Time', 'PT')]))
    preferred_qualifications = db.Column(db.String(100))
    medical_conditions = db.Column(db.String(100))

    def is_active(self):
        return self.is_enabled


usermanager = UserManager(None, None, None)
