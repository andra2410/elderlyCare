from flask import render_template, Blueprint

auth_blueprint = Blueprint("auth", __name__)
home_blueprint = Blueprint("home", __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # ........
    return render_template('login.html')


def register():
    # .........
    return render_template('register.html')
