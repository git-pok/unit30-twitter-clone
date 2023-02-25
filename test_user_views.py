"""Message model tests."""
# run these tests like:
# FLASK_ENV=production python -m unittest <name-of-python-file>
# python -m unittest test_user_model.py
from app import app
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from datetime import datetime
from models import db, User, Message, Follows

# environmental variable for test database
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

from app import app

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Test User views."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def tearDown(self):
        """Tear down sample data."""
        db.session.rollback()

    def test_user_views(self):
        """Tests model's views."""

        signup1 = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        )

        db.session.add(signup1)
        db.session.commit()

        with self.client as client:
            self.maxDiff=None
            client.get('/logout')
            credentials = {"username": 'testuser', "password": 'HASHED_PASSWORD'}
            resp = client.post('/login', data=credentials, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(
            '<div class="alert alert-success">Hello, testuser!</div>'
            , html
            )
            

    
    # def test_message_model_instances(self):
    #     """Tests model's instances."""
    #     u = User(
    #         email="test@test.com",
    #         username="testuser",
    #         password="HASHED_PASSWORD"
    #     )

    #     db.session.add(u)
    #     db.session.commit()

    #     id = u.id

    #     msg = Message(
    #         text="test text",
    #         user_id=id,
    #         timestamp=datetime.utcnow()
    #     )

    #     db.session.add(msg)
    #     db.session.commit()

    #     # Message object should have data
    #     self.assertEqual(msg, msg)
    #     self.assertEqual(msg.text, 'test text')
    #     self.assertEqual(msg.id, 2)