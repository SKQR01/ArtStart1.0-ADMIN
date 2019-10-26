from app import db
from datetime import datetime
import re
from flask_security import  UserMixin, RoleMixin

### Слаг ###
legend = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': 'y',
    'ы': 'y',
    'ь': "'",
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',

    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'Yo',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'H',
    'Ц': 'Ts',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Shch',
    'Ъ': 'Y',
    'Ы': 'Y',
    'Ь': "'",
    'Э': 'E',
    'Ю': 'Yu',
    'Я': 'Ya',
}


# транслит для слага
def translit(letter, dic):
    for i, j in dic.items():
        letter = letter.replace(i, j)
    return letter


# slug
def slugify(str):
    str = translit(str, legend)
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', str)


### Зависимости ###
posts_tags = db.Table(
    'posts_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

pictures_posts = db.Table(
    'pictures_posts',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('pictures_id', db.Integer, db.ForeignKey('picture.id'))

)

posts_user = db.Table(
    'posts_user',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

user_avatar = db.Table(
    'user_avatar',
    db.Column('picture_id', db.Integer, db.ForeignKey('picture.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


# class UserLikes(db.Model):
#     user_id = db.Column(db.Integer)
#     post_id = db.Column(db.Integer)

class user_likes(db.Model):
    row_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer)
    p_id = db.Column(db.Integer)


user_comments = db.Table(
    'user_comments',
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

post_comments = db.Table(
    'post_comments',
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
### Таблицы ###

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    createDate = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship('Tag', secondary=posts_tags, backref=db.backref('posts', lazy='dynamic'))
    pictures = db.relationship('Picture', secondary=pictures_posts, backref=db.backref('posts', lazy='dynamic'))
    user = db.relationship('User', secondary=posts_user)
    likes = db.Column(db.Integer)
    comment = db.relationship('Comment', secondary=post_comments, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *argc, **kwargs):
        super(Post, self).__init__(*argc, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post id: {}, title: {}, tags: {}>'.format(self.id, self.title, self.tags)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return '{}'.format(self.name)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *argc, **kwargs):
        super(Tag, self).__init__(*argc, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return '{}'.format(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    avatar = db.relationship('Picture', secondary=user_avatar, backref=db.backref('users',
                                                                                  lazy='dynamic'))  # переменная для привязки аватаров пользователей
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    posts = db.relationship('Post', secondary=posts_user, backref=db.backref('users', lazy='dynamic'))
    slug = db.Column(db.String(140), unique=True)
    description = db.Column(db.String(200))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, *argc, **kwargs):
        super(User, self).__init__(*argc, **kwargs)
        self.generate_slug()

    def is_authenticated():
        return True

    def generate_slug(self):
        if self.nickname:
            self.slug = slugify(self.nickname)



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.relationship('User', secondary=user_comments, backref=db.backref('comments', lazy='dynamic'))
    text = db.Column(db.String(250))
    create_date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '{}'.format(self.text)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
