from unittest import TestCase
from app import app
from models import db, User, Message

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class test_user_views(TestCase):
    def setup(self):
        Userquery.delete()


    def tearDown(self):
        db.session.rollback()
        User.query.delete()
        