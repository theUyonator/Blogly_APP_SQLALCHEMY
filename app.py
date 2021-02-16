"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SECRET_KEY'] = "top_secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)

##################################### User Routes ############################
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

######################## Post Routes ###################################

@app.route("/users/<int:user_id>/posts/new")
def show_newpost_form(user_id):
    """This view function shows a form to add a post for an existing user"""
    user = User.query.get_or_404(user_id)
    full_name = User.get_full_name(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, full_name = full_name, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """This view function adds a new post to the blogly db"""

    title = request.form["title"]
    content = request.form["content"]
    user_id = user_id
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/user/{user_id}")


@app.route("/posts/<int:post_id>")
def post_details(post_id):
    """This view function, shows the users post"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template("post_details.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit")
def show_editpost_form(post_id):
    """This view function shows a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)

    tags = Tag.query.all()

    return render_template("edit_post_form.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """This view function shows a form to edit an existing post"""
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content 
    post.tags = tags

    db.session.commit()

    return redirect(f"/user/{post.user_id}")

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """This view function deletes a post from the blogly db"""

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect("/users")


####################### Tag Routes ##########################################

@app.route("/tags")
def get_tags():
    """This view function, shows a list  of all available tags"""

    tags = Tag.query.all()

    return render_template("tags.html", tags=tags)



@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """This view function shows all posts associated with a given tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template("tag_details.html", tag=tag, posts=posts)

@app.route("/tags/new")
def add_tag():
    """This view function shows a form to add tags"""

    posts = Post.query.all()

    return render_template("new_tag.html", posts=posts)

@app.route("/tags/new", methods=["POST"])
def create_tag():
    """This view function creates a new in the blogly db"""

    tag_name = request.form["tag_name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    tag = Tag(tag_name = tag_name, posts=posts)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """This view function renders form used to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("edit_tag_form.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """This view function makes changes to an existing tag and makes sure it isaved in the blogly db"""
    
    tag_name = request.form["tag_name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    tag = Tag.query.get_or_404(tag_id)

    tag.tag_name = tag_name
    tag.posts = posts

    db.session.commit()

    return redirect(f"/tags/{tag_id}")

@app.route("/tags/<int:tag_id>/delete")
def delete_tag(tag_id):
    """This view function deletes a tag from the blogly db"""

    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect("/tags")