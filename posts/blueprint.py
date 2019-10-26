from flask import Blueprint, render_template, request, redirect, url_for, Response, json
from app import app, db
from PIL import Image
from mod import Post, Picture, Tag, Comment, User, user_likes
import os
from werkzeug.utils import secure_filename
from flask_login import current_user


posts = Blueprint('posts', __name__, template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@posts.route('/')
def index():
    page = request.args.get('page')
    
    q = request.args.get('q')

    if q:
        post = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        post = Post.query.order_by(Post.createDate.desc())


    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
     
    pages = post.paginate(page=page, per_page=15)

    return render_template('posts/index.html', post=post, pages=pages)


@posts.route('/create', methods=['GET', 'POST'])
def create_post():
    tags = Tag.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        file = request.files['file']

        user = current_user

        for t in request.form.getlist('tags'):
            tag = Tag.query.filter(Tag.name == t).first()

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_prev= Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_prev.save(os.path.join(app.config['UPLOAD_FOLDER'] + '\\post_prev', filename), quality=15,optimize=True)


            pic = Picture(name = filename)
            db.session.add(pic)
            db.session.commit()

            try:
                post = Post(title=title, body=body, likes=0)
                post.pictures.append(pic)
                post.tags.append(tag)
                post.user.append(user)

                db.session.add(post)
                db.session.commit()
            except:
                return 'Something wrong!'
        return redirect(url_for('posts.index'))
    else:
        return render_template('posts/create_post.html', tags=tags)

# @posts.route('/<slug>')
# def post_detail(slug):
#     post = Post.query.filter(Post.slug == slug).first_or_404()
#     tags = post.tags
#
#     return render_template('posts/post_detail.html', post=post, tags=tags)


@posts.route('/<id>')
def post_detail(id):
    post = Post.query.filter(Post.id == id).first_or_404()
    tags = post.tags

    if current_user.is_authenticated:
        user = current_user
        query = user_likes.query.filter(user_likes.u_id == user.id, user_likes.p_id == post.id).first()
        if query:
            is_like_set = True
        else:
            is_like_set = False
    else:
        is_like_set = False

    return render_template('posts/post_detail.html', post=post, tags=tags, is_like_set=is_like_set)

@posts.route('/<id>/add_like')
def add_like(id):
    post = Post.query.filter(Post.id == id).first_or_404()
    user = current_user

    if current_user.is_authenticated:
        query = user_likes.query.filter(user_likes.p_id == post.id, user_likes.u_id == user.id).first()
        if query:
            post.likes -= 1
            db.session.delete(query)
            is_like_set = False
        else:
            post.likes += 1
            row=user_likes(u_id=user.id, p_id=post.id)
            db.session.add(row)
            is_like_set = True
        db.session.commit()
    else:
        is_like_set = False
    response = {
        "likes" : post.likes,
        "is_like_set" : is_like_set,
    }

    return json.dumps(response)

@posts.route('/<id>/add_comment', methods=['GET', 'POST'])
def add_comment(id):
    if current_user:
        post = Post.query.filter(Post.id == id).first_or_404()
        user = current_user

        for i in user.avatar:
            ava = str(i)

        text_comment = request.args.getlist("text")
        current_comment = Comment(text=text_comment[0])
        current_comment.author.append(user)
        post.comment.append(current_comment)

        db.session.add(current_comment)

        db.session.commit()
        response = {
            'nickname': user.nickname,
            'userAvatar': ava,
        }
        return json.dumps(response)

 

@posts.route('/tag/<slug>')
def tag_detail(slug):
    page = request.args.get('page')

    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts


    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page, per_page=15)

    return render_template('posts/tag_detail.html', tag=tag, posts=posts, pages=pages)


# @posts.route('/')
# def index():
#     page = request.args.get('page')
#
#     q = request.args.get('q')
#
#     if q:
#         post = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
#     else:
#         post = Post.query.order_by(Post.createDate.desc())
#
#     if page and page.isdigit():
#         page = int(page)
#     else:
#         page = 1
#
#     pages = post.paginate(page=page, per_page=15)
#
#     return render_template('posts/index.html', post=post, pages=pages)