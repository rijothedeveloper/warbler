from unittest import TestCase
from app import app
from models import db, User, connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False

# connect_db(app)

db.drop_all()
db.create_all()

class test_app(TestCase):
    
    def setup(self):
        User.query.delete()


    def tearDown(self):
        db.session.rollback()
        User.query.delete()
        
    def test_signup(self):
        with app.test_client() as client:
            res = client.get("/")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            shouldContain = 'h4>New to Warbler?</h4>'
            self.assertIn(shouldContain, html)
            
            res = client.get("/signup")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            shouldContain = 'Username'
            self.assertIn(shouldContain, html)
            
            resp = client.post("/signup",
                               data={ 
                                     'email': "test2@test.com", 
                                     'username': "test2user", 
                                     'password': "mypass",
                                     'image_url': None } ,
                               follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            html = resp.get_data(as_text=True)
            shouldContain = 'test2user'
            self.assertIn(shouldContain, html)
        