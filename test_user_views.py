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

        signup = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        )
        db.session.add(signup)
        db.session.commit()
        self.signup = signup
    
    def tearDown(self):
        """Clear session data."""
        db.session.rollback()

    def test_login(self):
        """Tests model's login view."""
        with self.client as client:
            client.get('/')

            self.assertEqual(
                session.get("curr_user")
                , None
            )

            credentials = {
                            "username": self.signup.username,
                            "password": 'HASHED_PASSWORD'
                        }
            resp = client.post('/login', data=credentials, follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            # print("SIGN UP ID", self.signup.id)
            self.assertEqual(session.get("curr_user"), self.signup.id)

            user_query = User.query.filter_by(username = self.signup.username).first()
            self.assertEqual(user_query.email, self.signup.email)

    def test_login_fail(self):
        """Tests model's login view for fail."""
        with self.client as client:
            client.get('/')
            # curr_user should not be in session 
            self.assertEqual(session.get("curr_user"), None)
            credentials = {
                            "username": self.signup.username,
                            "password": 'WRONG_PASSWORD'
                        }
            resp = client.post('/login', data=credentials, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            # curr_user should not be in session
            self.assertEqual(session.get("curr_user"), None)