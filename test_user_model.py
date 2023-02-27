"""User model tests."""
# run these tests like:
# FLASK_ENV=production python -m unittest <name-of-python-file>
# python -m unittest test_user_model.py

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from models import db, User, Message, Follows

# environmental variable for test database
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Added line 22.
db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test User model."""

    def setUp(self):
        """Delete queries."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

    # Added tearDown and all logic in it.    
    def tearDown(self):
        """Clear session data."""
        db.session.rollback()


    def test_user_model_relationship(self):
        """Tests model's relationships."""

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
        # Added line 57.
        self.assertEqual(len(u.likes), 0)

    # Added all test methods and logic from here on.    
    def test_user_model_instances(self):
        """Tests model's instances."""
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
        """Tests model's following instance methods."""
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
        """Tests model's signup class method."""
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
        """Tests model's signup class method with exisitng credentials."""
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


    def test_user_model_authenticate(self):
        """Tests model's authenticate class method."""
        signup1 = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        )

        db.session.add(signup1)
        db.session.commit()

        self.assertEqual(
            User.authenticate(
            username="testuser", password="HASHED_PASSWORD"
            ), signup1
        )

        
    def test_user_model_invalid_authenticate(self):
        """Tests model's authenticate method with exisitng credentials."""
        signup1 = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        )

        db.session.add(signup1)
        db.session.commit()

        self.assertEqual(
            User.authenticate(
            username="testuser", password="WRONG_HASHED_PASSWORD"
            ), False
        )