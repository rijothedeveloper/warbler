from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class test_user_model(TestCase):

    def setup(self):
        User.query.delete()


    def tearDown(self):
        db.session.rollback()
        User.query.delete()

    def test_user_model(self):
        u = User(
            email="test@test.com",
            username="testuser",
            password="mypass"
        )
        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        
        repr = u.__repr__()
        expected = '<User #1: testuser, test@test.com>'
        self.assertEqual(repr,expected)
        
        otherUser = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        
        u.following.append(otherUser)
        db.session.commit()
        
        self.assertEqual(u.is_following(otherUser), True)
        self.assertEqual(otherUser.is_following(u), False)
        
        self.assertEqual(u.is_followed_by(otherUser), False)
        self.assertEqual(otherUser.is_followed_by(u), True)
        
        # self.assertNotEqual(u.authenticate(u.username,"mypass"), None)
        
    def test_authentication(self):
        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="mypass",
            image_url=""
        )
        self.assertNotEqual(u.authenticate(u.username,"mypass"), False)
        self.assertEqual(u.authenticate(u.username,"wrong pass"), False)
        self.assertEqual(u.authenticate("wrong user","mypass"), False)
        
        
        
    
        