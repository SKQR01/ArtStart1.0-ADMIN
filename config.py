import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


### Класс конфигурации ###
class Conf(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR + "\\data\\db.db"

    UPLOAD_FOLDER = BASE_DIR + "\\static\\img"
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webp'])

    SECURITY_PASSWORD_SALT = 'bcrypt'
    SECRET_KEY = 'Something secret'
