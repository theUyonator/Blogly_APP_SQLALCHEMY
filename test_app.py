from unittest import TestCase

from app import app
from models import db, User

# A test database is used so that our bd isn't cluttered 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

#To make flask errors real erros rather than HTML pages set TESTING configuration to True
app.config['TESTING'] = True

#Don't show debug toolbar 
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """This class contains methods that test the view functions of the blogly app"""

    def setUp(self):
        """Add sample User"""

        User.query.delete()

        user = User(first_name="Baker", last_name="Mayfield", image_url="https://www.sportscasting.com/wp-content/uploads/2020/02/Quarterback-Baker-Mayfield-Cleveland-Browns.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transcations."""

        db.session.rollback()

    def test_user_list(self):
        """This test methods test to see if the user list is being created"""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Baker', html)

    def test_add_user(self):
        """This test method test to see if a new user is being created and displayed once the add user form is submitted"""
        with app.test_client() as client:
            u = {"first_name": "Aaron", "last_name": "Rodgers", "img_url":"https://static.www.nfl.com/image/private/t_player_profile_landscape/f_auto/league/jbouklrht7n1r6afurdc"}
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Aaron Rodgers", html)

    # def test_user_details(self):
    #     """This test method tests if the user information is shown in the card"""
    #     user_id = 1
    #     with app.test_client() as client:
    #         resp = client.get("/user/" + user_id)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("This is Baker's profile", html)