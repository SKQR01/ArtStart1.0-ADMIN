from app import app
import view
import os

from posts.blueprint import posts
from users.blueprint import users


### Регистрация Blueprint-ов ###

app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(users, url_prefix='/users')


### Запуск приложения ###

if __name__ == '__main__':
    app.run(host='')