from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from flask_login import current_user, login_required, login_user, LoginManager
from flask_user.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

from .models import db, Users

auth_blueprint = Blueprint("auth", __name__, template_folder='templates')
home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/')
def homepage():
    if current_user.is_authenticated:
        if current_user.role == 'caregiver':
            return redirect(url_for('auth.caregiver_dashboard'))
        elif current_user.role == 'care-seeker':
            return redirect(url_for('auth.careseeker_dashboard'))
    return render_template('homepage.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def custom_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(db)
        user = Users.query.filter_by(username=username).first()

        #login_user(user, remember=True)
        session['role'] = 'NULL'
        session['username'] = 'NULL'

        if user:
            if check_password_hash(user.password, password):
                # Password matches, log in the user
                print('User authenticated:', user.username)
                # print(current_user.id)
                print('role', user.role)
                session['role'] = user.role
                session['username'] = username
                print('Current user authenticated:', current_user.is_authenticated)

                # Print session information
                print('Session:', session)

                # Redirect user based on role
                if user.role == 'caregiver':
                    print('Redirecting to caregiver dashboard')
                    return redirect(url_for('auth.caregiver_dashboard'))
                elif user.role == 'care_seeker':
                    print('Redirecting to care seeker dashboard')
                    return redirect(url_for('auth.careseeker_dashboard'))
                else:
                    flash('Invalid role.', 'error')
            else:
                flash('Invalid password.', 'error')
        else:
            # User not found in the database
            flash('User not found. Please register.', 'error')

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

        hashed_password = generate_password_hash(password)

        user = Users(
            username=username,
            email=email,
            password=hashed_password,
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
        login_user(user, remember=True)
        return redirect(url_for('home.homepage'))
    else:
        return render_template('register.html')


@auth_blueprint.route('/caregiver_dashboard')
# @login_required
def caregiver_dashboard():
    print('User authenticated before @login_required:', current_user.is_authenticated)
    print("Session:", session)
    # print("User role:", current_user.role)
    if session.get('role') == 'caregiver':
        care_seekers = Users.query.filter_by(role='care_seeker').all()
        return render_template('caregiver_dashboard.html', care_seekers=care_seekers)
    else:
        flash('Access denied. Log in as careseeker', 'error')
        return redirect(url_for('home.homepage'))


@auth_blueprint.route('/careseeker_dashboard')
# @login_required
def careseeker_dashboard():
    if session.get('role') == 'care_seeker':
        caregivers = Users.query.filter_by(role='caregiver').all()
        return render_template('careseeker_dashboard.html', caregivers=caregivers)
    else:
        flash('Access denied. Log in as caregiver', 'error')
        return redirect(url_for('home.homepage'))


@home_blueprint.route('/about')
def about():
    return render_template('about.html')


@home_blueprint.route('/contact')
def contact():
    return render_template('contact.html')


@auth_blueprint.route('/caregivers_profile/<username>', methods=['GET', 'POST'])
def caregivers_profile(username):
    if 'role' in session and session['role'] == 'caregiver':
        user = Users.query.filter_by(username=username, role='caregiver').first()
        if request.method == 'POST':
            new_username = request.form.get('new_username')
            new_email = request.form.get('new_email')
            new_location = request.form.get('new_location')
            new_age = request.form.get('new_age')
            new_experience = request.form.get('new_experience')
            new_references_text = request.form.get('new_references')
            new_availability = request.form.get('new_availability')
            new_languages_spoken = request.form.get('new_languages_spoken')
            new_background_check = request.form.get('new_background_check')
            new_additional_notes = request.form.get('new_additional_notes')

            if new_username != user.username and Users.query.filter_by(username=new_username).first():
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('caregivers_profile.html', user=user)
            else:
                user.username = new_username
            if new_email:
                user.email = new_email
            if new_location:
                user.location = new_location
            if new_age:
                user.age = new_age
            if new_experience:
                user.experience = new_experience
            if new_availability:
                user.availability = new_availability
            if new_languages_spoken:
                user.languages_spoken = new_languages_spoken
            if new_background_check:
                user.background_check = new_background_check == 'True'  # Convert to boolean
            if new_references_text:
                user.references = new_references_text
            if new_additional_notes:
                user.additional_notes = new_additional_notes

            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('auth.caregivers_profile', username=username))
        else:
            return render_template('caregivers_profile.html', user=user)
    else:
        flash('Login first', 'error')
        return redirect(url_for('home.homepage'))


@auth_blueprint.route('/careseeker_profile/<username>', methods=['GET', 'POST'])
def careseeker_profile(username):
    if 'role' in session and session['role'] == 'care_seeker':
        print(session['role'])
        print(session['username'])
        user = Users.query.filter_by(username=username, role='care_seeker').first()
        if request.method == 'POST':
            new_username = request.form.get('new_username')
            new_email = request.form.get('new_email')
            new_location = request.form.get('new_location')
            new_age = request.form.get('new_age')
            new_type_of_care_needed = request.form.get('new_type_of_care_needed')
            new_medical_conditions = request.form.get('new_medical_conditions')
            new_preferred_qualifications = request.form.get('new_preferred_qualifications')
            new_monthly_budget = request.form.get('new_monthly_budget')
            new_availability_needed = request.form.get('new_availability_needed')

            if new_username != user.username and Users.query.filter_by(username=new_username).first():
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('careseeker_profile.html', user=user)
            else:
                user.username = new_username
            if new_email:
                user.email = new_email
            if new_location:
                user.location = new_location
            if new_age:
                user.age = new_age
            if new_type_of_care_needed:
                user.type_of_care_needed = new_type_of_care_needed
            if new_availability_needed:
                user.availability_needed = new_availability_needed
            if new_monthly_budget:
                user.monthly_budget = new_monthly_budget
            if new_preferred_qualifications:
                user.preferred_qualifications = new_preferred_qualifications
            if new_medical_conditions:
                user.medical_conditions = new_medical_conditions

            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('auth.careseeker_profile', username=username))
        else:
            return render_template('careseeker_profile.html', user=user)
    else:
        flash('Login first', 'error')
        return redirect(url_for('home.homepage'))


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
