"""Seed file to make sample data for the blogly db"""

from models import User, db
from app import app

# Create all tables

db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()

# Add users 

Deshaun = User(first_name = "DeShaun", last_name = "Watson", image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvRtQVYJ0NHS14G_ve72YV8Vjg5DCePxLwJA&usqp=CAU")

Mahomes = User(first_name = "Patrick", last_name = "Mahomes", image_url = "https://static.clubs.nfl.com/image/private/t_editorial_landscape_12_desktop/chiefs/iwmsg6lhulvntsg327gk")

Kyler = User(first_name = "Kyler", last_name = "Murray", image_url = "https://static.clubs.nfl.com/image/private/t_editorial_landscape_8_desktop_mobile/f_auto/cardinals/qcrq0eqmx9lsmqyjchiv.jpg")

Lamar = User(first_name = "Lamar", last_name = "Jackson", image_url = "https://images.fantasypros.com/images/players/nfl/17233/headshot/1200x1200.png")


#Now we add the objects to seession, so they'll persist

db.session.add(Deshaun)
db.session.add(Mahomes)
db.session.add(Kyler)
db.session.add(Lamar)

# To save these in the db we commit 
db.session.commit()