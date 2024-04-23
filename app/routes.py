from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from .models import db, Users

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

        user = Users.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                if user.role == 'caregiver':
                    return redirect(url_for('auth.caregiver_dashboard'))
                elif user.role == 'care_seeker':
                    return redirect(url_for('auth.careseeker_dashboard'))
                else:
                    flash('Invalid role.', 'error')
            else:
                flash('Invalid password.', 'error')
        else:
            flash('User not found.', 'error')

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

        if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
            flash('Username or email already exists. Please choose a different one.', 'error')
            return redirect(url_for('auth.register'))

        if role == 'caregiver':
            availability = request.form.get('availability')
            background_check = request.form.get('background_check') == 'Yes'
            availability_needed = None

        else:
            availability_needed = request.form.get('availability_needed')
            availability = None
            background_check = None

        user = Users(
            username=username,
            email=email,
            password=password,
            location=location,
            phone_number=phone_number,
            role=role,

            # Set caregiver-specific fields if role is caregiver
            experience=request.form.get('experience'),
            references=request.form.get('references'),
            availability=availability,
            languages_spoken=request.form.get('languages_spoken'),
            background_check=background_check,
            additional_notes=request.form.get('additional_notes'),

            # Set care seeker-specific fields if role is care seeker
            type_of_care_needed=request.form.get('type_of_care_needed'),
            monthly_budget=request.form.get('budget'),
            availability_needed=availability_needed,
            preferred_qualifications=request.form.get('preferred_qualifications'),
            medical_conditions=request.form.get('medical_conditions'),
        )

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home.homepage'))
    else:
        return render_template('register.html')


@auth_blueprint.route('/caregiver_dashboard')
def caregiver_dashboard():
    care_seekers = Users.query.filter_by(role='care_seeker').all()
    return render_template('caregiver_dashboard.html', care_seekers=care_seekers)


@auth_blueprint.route('/careseeker_dashboard')
def careseeker_dashboard():
    return render_template('careseeker_dashboard.html')


# @auth_blueprint.route('/')
# def index():
#     new_user = Users(
#         username='admin',
#         password='admin',
#         email='admin@admin.com',
#         location='buc',
#         phone_number='0000000000',
#         role='admin',
#         age=20)
#     db.session.add(new_user)
#     db.session.commit()
#     flash('Invalid username or password', 'error')
