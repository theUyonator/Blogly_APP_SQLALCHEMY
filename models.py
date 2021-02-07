"""Models for Blogly."""
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





    
