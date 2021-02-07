from unittest import TestCase

from app import app
from models import db, User

# A test database is used so that our bd isn't cluttered 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for the User model"""

    def setUp(self):
        """Clean up any existing users"""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transactions"""

        db.session.rollback()

    def test_get_full_name(self):
        """Test the class method that creates the full name"""

        user = User(first_name="Travis", last_name="Kelce", image_url="http://www.yardbarker.com/media/a/9/a9ce0d7db44e3b19d9f4defbb35f2115d35dab88/thumb_16x9/report-travis-kelce-chiefs-closing-on-long-term.jpg?v=1")
        db.session.add(user)
        db.session.commit()

        full_name = User.get_full_name(user.id)
        self.assertEquals(full_name, "Travis Kelce")
