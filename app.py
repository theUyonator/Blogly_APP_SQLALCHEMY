"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = "top_secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)


@app.route("/")
def homepage():
    """This view function redirects to the user listings"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND PAGE"""

    return render_template('404.html'), 404

@app.route("/users")
def user_listings():
    """This view function shows all users for this app"""

    users = User.query.all()
    return render_template("users.html", users = users)


@app.route("/users/new")
def show_newuser_form():
    """This view function shows a form to add new user"""

    return render_template("new_user_form.html")

@app.route("/users/new", methods=["POST"])
def add_new_user():
    """This view function adds a new user to the blogly db"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['img_url']
    image_url = image_url if image_url else None

    user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/user/<int:user_id>")
def user_details(user_id):
    """This view function shows user details"""
    
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    full_name = User.get_full_name(user_id)
    return render_template("user_details.html", user=user, full_name = full_name, posts = posts)

@app.route("/users/<int:user_id>/edit")
def show_useredit_form(user_id):
    """This view function shows a form to edit an existing user's information"""

    return render_template("user_edit_form.html", user_id = user_id)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """This view function edits an existing user's information and saves it to the db"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['img_url']
    image_url = image_url if image_url else None

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """This view function deletes an existing user's information from blogly db"""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def show_newpost_form(user_id):
    """This view function shows a form to add a post for an existing user"""
    user = User.query.get_or_404(user_id)
    full_name = User.get_full_name(user_id)
    return render_template("new_post.html", user=user, full_name = full_name)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """This view function adds a new post to the blogly db"""

    title = request.form["title"]
    content = request.form["content"]
    user_id = user_id

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/user/{user_id}")


@app.route("/posts/<int:post_id>")
def post_details(post_id):
    """This view function, shows the users post"""

    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_editpost_form(post_id):
    """This view function shows a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)

    return render_template("edit_post_form.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """This view function shows a form to edit an existing post"""
    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content 

    db.session.commit()

    return redirect(f"/user/{post.user_id}")

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """This view function deletes a post from the blogly db"""

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect("/users")



