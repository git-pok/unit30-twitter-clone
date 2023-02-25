"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def tearDown(self):
        """Create test client, add sample data."""
        db.session.rollback()

    def test_user_model_relationship(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages, followers, and likes
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.likes), 0)
    
    def test_user_model_repr(self):
        """Does basic model work?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User object should have data
        self.assertEqual(u, u)
        self.assertEqual(u.email, 'test@test.com')
        self.assertEqual(u.username, 'testuser')

    def test_user_model_following(self):
        """Does basic model work?"""
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.assertEqual(u1.is_following(u2), False)
        self.assertEqual(u1.is_followed_by(u2), False)

        follow1 = Follows(user_being_followed_id=u1.id, user_following_id=u2.id)
        db.session.add(follow1)
        db.session.commit()
        self.assertEqual(u1.is_followed_by(u2), True)

    def test_user_model_signup(self):
        """Does basic model work?"""
        signup1 = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        )

        db.session.add(signup1)
        db.session.commit()

        self.assertEqual(signup1, signup1)

    def test_user_model_signup_with_existing_user(self):
        """Does basic model work?"""
        signup1 = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        )

        db.session.add(signup1)
        db.session.commit()

        signup2 = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        )
        db.session.add(signup2)
        self.assertRaises(IntegrityError, db.session.commit)