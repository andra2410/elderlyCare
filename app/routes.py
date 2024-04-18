from flask import Flask, Blueprint, render_template, request, redirect, url_for

from app import Caregivers
from .models import db, CareSeekers

auth_blueprint = Blueprint("auth", __name__, template_folder='templates')
home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/')
def homepage():
    return render_template('homepage.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # ........
    return render_template('login.html')


@auth_blueprint.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        phone_number = request.form['phone_number']
        role = request.form['role']

        if role == 'caregiver':
            experience = request.form['experience']
            references = request.form['references']
            availability = request.form['availability']
            languages_spoken = request.form['languages_spoken']
            background_check = 'background_check' in request.form
            additional_notes = request.form['additional_notes']

            caregiver = Caregivers(username=username, email=email, password=password,
                                   location=location, phone_number=phone_number,
                                   experience=experience, references=references,
                                   availability=availability, languages_spoken=languages_spoken,
                                   background_check=background_check, additional_notes=additional_notes)
            db.session.add(caregiver)

        elif role == 'care_seeker':
            age = request.form['age']
            type_of_care_needed = request.form['type_of_care_needed']
            monthly_budget = request.form['budget']  # Corrected field name
            availability_needed = request.form['availability_needed']
            preferred_qualifications = request.form['preferred_qualifications']
            medical_conditions = request.form['medical_conditions']

            care_seeker = CareSeekers(username=username, email=email, password=password,
                                      location=location, phone_number=phone_number,
                                      age=age, type_of_care_needed=type_of_care_needed,
                                      monthly_budget=monthly_budget,
                                      availability_needed=availability_needed,
                                      preferred_qualifications=preferred_qualifications,
                                      medical_conditions=medical_conditions)
            db.session.add(care_seeker)

        db.session.commit()
        return redirect(url_for('home.homepage'))
    else:
        return render_template('register.html')
