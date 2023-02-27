"""User model views tests."""
# Added everything in this file.
# run these tests like:
# FLASK_ENV=production python -m unittest <name-of-python-file>
# python -m unittest test_user_model.py
import os
from flask import session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from datetime import datetime
from models import db, User, Message, Follows

# environmental variable for test database
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """Test User views."""
    def setUp(self):
        """Create test client, and delete queries."""
        db.drop_all()
        db.create_all()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def tearDown(self):
        """Clear session data."""
        db.session.rollback()
        # db.drop_all()

    def test_login(self):
        """Tests model's login view."""

        signup = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        ) 

        db.session.add(signup)
        db.session.commit()

        with self.client as client:
            client.get('/')

            self.assertEqual(
                session.get("curr_user")
                , None
            )

            credentials = {"username": 'testuser', "password": 'HASHED_PASSWORD'}
            resp = client.post('/login', data=credentials, follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            
            self.assertEqual(
                session.get("curr_user")
                , 1
            )

            user_query = User.query.one()
            self.assertEqual(user_query.email, "test@test.com")

    def test_login_fail(self):
        """Tests model's login view for fail."""

        signup = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        ) 

        db.session.add(signup)
        db.session.commit()

        with self.client as client:

            client.get('/')

            # curr_user should not be in session 
            self.assertEqual(
                session.get("curr_user")
                , None
            )

            credentials = {"username": 'testuser', "password": 'WRONG_HASHED_PASSWORD'}
            resp = client.post('/login', data=credentials, follow_redirects=True)
            
            # curr_user should not be in session
            self.assertEqual(
                session.get("curr_user")
                , None
            )

            self.assertEqual(resp.status_code, 200)

                # g.user = signup
                # pdb.set_trace()
                # html = likes_resp.get_data() 
                # self.assertEqual('<h1></h1>', html)

                # self.maxDiff=None
                # Keep getting error when testing html, its too long
                # I went to pdb, then tried data; it did not work
                # html = likes_resp.get_data(as_text=True)
                # self.maxDiff=None
                # self.assertEqual('<h1></h1>', html) 