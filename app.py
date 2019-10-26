from flask import Flask, request, url_for, redirect
from config import Conf
from flask_sqlalchemy import SQLAlchemy
import sqlite3

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask import Blueprint, render_template, redirect, url_for
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, Security, SQLAlchemyUserDatastore, url_for_security

### Инициализация приложения ###

app = Flask(__name__)
app.config.from_object(Conf)

### Создание БД ###

db = SQLAlchemy(app)

### Создание курсосра и соединения с БД ###

conn = sqlite3.connect(r"data/db.db")
cursor = conn.cursor()

login_manager = LoginManager(app)
login_manager.init_app(app)

### Миграции ###
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

### Админка ###
from mod import *

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('security.login', next=request.url))

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'ArtStart',index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Tag, db.session))

# admin.add_view(ModelView(Post, db.session))
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Tag, db.session))
