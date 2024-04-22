from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_user import login_required
from flask_login import login_user, login_manager, current_user
from flask_mail import Message

from app import Caregivers
from .models import db, CareSeekers

auth_blueprint = Blueprint("auth", __name__, template_folder='templates')
home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/')
def homepage():
    return render_template('homepage.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Search for the user in both Caregivers and CareSeekers tables
        caregiver = Caregivers.query.filter_by(username=username).first()
        care_seeker = CareSeekers.query.filter_by(username=username).first()

        # Check if the user exists in either table
        if caregiver and caregiver.password == password:
            return redirect(url_for('auth.caregiver_dashboard'))
        elif care_seeker and care_seeker.password == password:
            return redirect(url_for('auth.careseeker_dashboard'))
        else:
            flash('Invalid username or password', 'error')
            # return redirect(url_for('auth.login'))
    return redirect(url_for('home.homepage'))


@auth_blueprint.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        phone_number = request.form['phone_number']
        role = request.form['role']

        if Caregivers.query.filter_by(username=username).first() or CareSeekers.query.filter_by(
                username=username).first():
            flash('Username already exists. Please choose a different username', 'error')
            return redirect(url_for('auth.register'))

        if Caregivers.query.filter_by(email=email).first() or CareSeekers.query.filter_by(email=email).first():
            flash('Email already in use. Try logging in instead.', 'error')

        if role == 'caregiver':
            experience = request.form['experience']
            age = request.form['age']
            references = request.form['references']
            availability = request.form['availability']
            languages_spoken = request.form['languages_spoken']
            background_check = 'background_check' in request.form
            additional_notes = request.form['additional_notes']

            caregiver = Caregivers(username=username,
                                   age=age,
                                   email=email,
                                   password=password,
                                   location=location,
                                   phone_number=phone_number,
                                   experience=experience,
                                   references=references,
                                   availability=availability,
                                   languages_spoken=languages_spoken,
                                   background_check=background_check,
                                   additional_notes=additional_notes,
                                   role='caregiver')
            db.session.add(caregiver)

        elif role == 'care_seeker':
            age = request.form['age']
            type_of_care_needed = request.form['type_of_care_needed']
            monthly_budget = request.form['budget']  # Corrected field name
            availability_needed = request.form['availability_needed']
            preferred_qualifications = request.form['preferred_qualifications']
            medical_conditions = request.form['medical_conditions']

            care_seeker = CareSeekers(username=username,
                                      email=email,
                                      password=password,
                                      location=location,
                                      phone_number=phone_number,
                                      age=age,
                                      type_of_care_needed=type_of_care_needed,
                                      monthly_budget=monthly_budget,
                                      availability_needed=availability_needed,
                                      preferred_qualifications=preferred_qualifications,
                                      medical_conditions=medical_conditions,
                                      role='care-seeker')
            db.session.add(care_seeker)

        db.session.commit()
        return redirect(url_for('home.homepage'))
    else:
        return render_template('register.html')


@auth_blueprint.route('/caregiver_dashboard')
def caregiver_dashboard():
    care_seekers = CareSeekers.query.all()
    return render_template('caregiver_dashboard.html', care_seekers=care_seekers)


@auth_blueprint.route('/careseeker_dashboard')
def careseeker_dashboard():
    caregivers = Caregivers.query.all()
    return render_template('careseeker_dashboard.html', caregivers=caregivers)
