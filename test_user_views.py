"""Message model tests."""
# run these tests like:
# FLASK_ENV=production python -m unittest <name-of-python-file>
# python -m unittest test_user_model.py
import os
from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from datetime import datetime
from models import db, User, Message, Follows

# environmental variable for test database
# tests still effect real database
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False
# db.drop_all() still effects real database
# db.drop_all()
# db.create_all()

class UserViewsTestCase(TestCase):
    """Test User views."""
    # db.drop_all()
    # db.create_all()
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def tearDown(self):
        """Tear down sample data."""
        db.session.rollback()
        # db.drop_all()

    def test_login(self):
        """Tests model's views."""

        signup = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        ) 

        db.session.add(signup)
        db.session.commit()

        with self.client as client:
            # import pdb
            # pdb.set_trace()
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

    def test_login_fail(self):
        """Tests model's views."""

        signup = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        ) 

        db.session.add(signup)
        db.session.commit()

        with self.client as client:
            # import pdb
            # pdb.set_trace()

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

    # def test_likes(self):
    #     """Tests model's views."""
    #     signup = User.signup(
    #         email="test@test.com",
    #         username="testuser",
    #         password="HASHED_PASSWORD",
    #         image_url="http//:www.testjpg.jpg"
    #     ) 

    #     db.session.add(signup)
    #     db.session.commit()

    #     with self.client as client:
    #         # import pdb
    #         # pdb.set_trace()
    #         client.get('/')

    #         self.assertEqual(
    #             session.get("curr_user")
    #             , None
    #         )

    #         credentials = {"username": 'testuser', "password": 'HASHED_PASSWORD'}
    #         resp = client.post('/login', data=credentials, follow_redirects=True)
            
    #         self.assertEqual(resp.status_code, 200)
            
    #         self.assertEqual(
    #             session.get("curr_user")
    #             , 1
    #         )

    #         likes_resp = client.get('/users/1/following')

            # self.maxDiff=None
            # Keep getting error when testing html, its too long
            # I went to pdb, then tried data; it did not work
            # html = likes_resp.get_data(as_text=True)
            # self.maxDiff=None
            # self.assertEqual('<h1></h1>', html) 