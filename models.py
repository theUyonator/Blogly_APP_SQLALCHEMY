"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """This Model holds information of the structure of the User table in the blogly db"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    first_name = db.Column(db.Text, nullable = False)

    last_name = db.Column(db.Text, nullable = False)

    image_url = db.Column(db.Text, nullable = True, default = "https://nicolasmelis.com/wp-content/themes/panama/assets/img/empty/600x600.png")


    def __repr__(self):
        """This method shows info about this particular instance of the User class"""

        p = self

        return f"<first_name = {p.first_name} last_name = {p.last_name} image_url = {p.image_url}>"

    @classmethod
    def get_full_name(cls, user_id):
        """This class get's both the first and last names of the user and forms a full name"""

        u = cls.query.get_or_404(user_id)
        u_first = u.first_name
        u_last = u.last_name 

        u_full = f"{u_first} {u_last}"

        return u_full



class Post(db.Model):
    """This model holds all information of the structure of the post table in the blogly db"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                    primary_key = True, 
                    autoincrement = True)

    title = db.Column(db.String(50), nullable = False)

    content = db.Column(db.String(100), nullable = False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    rel = db.relationship('User', cascade="all,delete", backref='posts')

    def __repr__(self):
        """This method shows info about this particular instance of the Post class"""

        p = self

        if p.title:
            return f"<title = {p.title} content = {p.content} created_at = {p.created_at}>"
        else:
            return f"<content = {p.content} created_at = {p.created_at}>"

    
    @property
    def friendly_date(self):
        """This returns a nicely formatted date."""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")



class Tag(db.Model):
    """This model holds all information of the structure of the tag table in the blogly db"""

    __tablename__="tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    tag_name = db.Column(db.Text,
                        nullable=False,
                        unique=True)
    posts = db.relationship("Post",
                            secondary="post_tags",
                            backref="tags",
                            cascade="all,delete")


    def __repr__(self):
        """This method shows info about this particular instance of the Tag class"""

        p = self

        return f"<tag_name = {p.tag_name}"


class PostTag(db.Model):
    """This model holds all information of the structure of the post_tags table holding the many_to_many relationship btw posts and tags in the blogly db"""

    __tablename__="post_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                        db.ForeignKey("tags.id"),
                        primary_key=True)

    
    def __repr__(self):
        """This method shows info about this particular instance of the PostTag class"""

        p = self

        return f"<post_id = {p.post_id} tag_id = {p.tag_id}"

    
