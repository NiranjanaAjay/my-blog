
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_ckeditor import CKEditor


load_dotenv()

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = os.environ["KEY"]
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

class NewPost(FlaskForm):
  title = StringField(label='Title of the blog', validators=[DataRequired()])
  subtitle = StringField(label='Subtitle', validators=[DataRequired()])
  body = CKEditorField(label='Content', validators=[DataRequired()])
  author = StringField(label='Author', validators=[DataRequired()])
  img = StringField(label='Image URL', validators=[URL()])
  submit = SubmitField(label='Done')


@app.route('/')
def get_all_posts():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalar()
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/add', methods=['GET','POST'])
def add_new_post():
    form = NewPost()
    edit_post = False
    if request.method == 'POST':
        if request.form.get("img")=='':
            image = ("https://images.unsplash.com/photo-1680299568009-09a6f8383061?q=80&w=1074&auto=format&fit"
                     "=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
        else:
            image = request.form.get("img")
        new_post = BlogPost(
            title = request.form.get("title"),
            subtitle = request.form.get("subtitle"),
            date = datetime.today().strftime("%d %B, %Y"),
            body = request.form.get("body"),
            author = request.form.get("author"),
            img_url = image
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")
    return render_template("make-post.html", form=form, edit = edit_post)


@app.route('/edit/<int:post_id>', methods=['GET','POST'])
def edit(post_id):
    if request.method == 'POST':
        post = db.session.get(BlogPost,post_id)
        if request.form.get("img")=='':
            image = ("https://images.unsplash.com/photo-1680299568009-09a6f8383061?q=80&w=1074&auto=format&fit"
                     "=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
        else:
            image = request.form.get("img")
        post.title = request.form.get("title")
        post.subtitle = request.form.get("subtitle")
        post.img_url = image
        post.author = request.form.get("author")
        post.body = request.form.get("body")
        db.session.commit()
        return redirect(f"/post/{post_id}")

    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    edit_form = NewPost(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    edit_post = True
    return render_template("make-post.html", form=edit_form, edit=edit_post)

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
