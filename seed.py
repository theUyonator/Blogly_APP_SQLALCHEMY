"""Seed file to make sample data for the blogly db"""

from models import User, Post, db
from app import app

# Create all tables

db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()
Post.query.delete()

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

#Add posts

shauns_statement = Post(title = "Texas we have a problem!", content = "I have wanted out of Texas for a while now, nothing can change my mind", user_id = 1)

shaun_on_culley = Post(title = "Culley can't stop me!", content = "This mf Culley think I'ma change my mind because of him?!, hell no!", user_id = 1)

Mahomes_superbowl = Post(title = "Brady the GOAT", content = "Man I wish I hadn't lost to Tom yo!, I'm heated rn!", user_id = 2)

Kyler_letting_go = Post(title = "Arizona on some BS!", content = "Man I am carrying this team on my back, me and DHOP!", user_id = 3)

Lamar_no_win = Post(content = "Man when will a brother like me win a SB dawg, I done tried you feel me!", user_id = 4)


db.session.add(shauns_statement)
db.session.add(shaun_on_culley)
db.session.add(Mahomes_superbowl)
db.session.add(Kyler_letting_go)
db.session.add(Lamar_no_win)


db.session.commit()

