from app import app, login_manager, db, user_datastore
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from mod import User, Picture, Post
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return 'Ватафак ю доинг хир?!'


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         form_user = request.form.get('login')
#         user = User.query.filter(User.nickname == form_user).first()
#         login_user(user)
#         return redirect(url_for('index'))
#     else:
#         return render_template('users/login.html')


@app.route('/register', methods=['GET', 'POST'])
def reg_user():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if User.query.filter(User.nickname == nickname).first():
            flash('Пользователь с таким именем уже зарегестрирован!')
            return render_template('users/user_register.html')

        if User.query.filter(User.email == email).first():
            flash('Пользователь с такой почтой уже зарегестрирован!')
            return render_template('users/user_register.html')

        if confirm_password == password:
            pic = Picture.query.filter(Picture.name == '.no_image.jpg').first()

            # u = User(nickname=nickname, email=email, password=password, active=True, description=' ')
            user_datastore.create_user(nickname=nickname, email=email, password=password, active=True, description=' ')
            user = User.query.filter(User.nickname == nickname).first()
            user.avatar.append(pic)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('users/user_register.html')
#

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.index'))


@app.route('/home')
@login_required
def home():
    user = current_user
    avatar = user.avatar

    posts = Post.query.filter(Post.user.contains(user)).all()

    return render_template('users/user_profile_home.html', user_profile=user, avatar=avatar, user_posts=posts)


@app.route('/home/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        file = request.files['avatar']

        description = request.form.get('description')
        current_user.description = description
        db.session.commit()

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + r'\avatars', filename))

            pic = Picture(name=filename)
            db.session.add(pic)

            if current_user.avatar:
                for i in current_user.avatar:
                    path = os.path.join(app.config['UPLOAD_FOLDER'] + r'\avatars\\'[:-1], i.name)
                    os.remove(path)
            try:
                current_user.avatar.clear()

                current_user.avatar.append(pic)
                db.session.commit()
                return redirect('/home')
            except:
                return 'Something wrong!'
        else:
            return redirect('/home')
    else:
        return render_template('users/user_profile_edit.html')
