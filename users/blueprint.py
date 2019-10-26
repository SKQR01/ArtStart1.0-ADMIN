from flask import Blueprint, render_template
from mod import User
from flask_login import current_user


users = Blueprint('users', __name__, template_folder='templates')

@users.route('/')
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@users.route('/<slug>')
def user_profile(slug):
    u  = User.query.filter(User.slug == slug).first()
    return render_template('users/user_profile.html', user_profile=u)


