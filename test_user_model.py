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


class UserModelTestCase(TestCase):
    """Test User model."""
    # Defined setUp and logic in it.
    def setUp(self):
        """Delete queries."""
        db.drop_all()
        db.create_all()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user1 = User(
            # id=1,
            email="test@test.com",
            username="testuser",
            password="HASHEDPASSWORD",
            image_url=""
        )
        # self.user1 = user1
        db.session.add(user1)
        db.session.commit()
        self.user1 = user1
        self.user1_id = self.user1.id

        user2 = User(
            email="test2@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        user3 = User(
            email="test3@test.com",
            username="test3user",
            password="HASHED_PASSWORD3"
        )
        db.session.add_all([user2, user3])
        db.session.commit()
        self.user2 = user2
        self.user3 = user3
        follow1 = Follows(user_being_followed_id=user2.id, user_following_id=user3.id)
        db.session.add(follow1)
        db.session.commit()

        signup1 = User.signup(
            email="testsignup@test.com",
            username="testsignupuser",
            password="HASHED_PASSWORDsignup",
            image_url="http//:www.testjpg.jpg"
        )
        db.session.add(signup1)
        db.session.commit()
        self.signup1 = signup1

    # Defined tearDown and all logic in it.    
    def tearDown(self):
        """Clear session data."""
        db.session.rollback()

    # Defined logic in test_user_model_relationship.
    def test_user_model_relationship(self):
        """Tests model's relationships."""
        self.assertEqual(len(self.user1.messages), 0)
        self.assertEqual(len(self.user1.followers), 0)
        self.assertEqual(len(self.user1.likes), 0)

    # DEFINED all test methods and logics from here on.    
    def test_user_model_instances(self):
        """Tests model's instances."""
        self.assertEqual(isinstance(self.user1, User), True)
        self.assertEqual(self.user1, self.user1)
        self.assertEqual(self.user1.email, 'test@test.com')
        self.assertEqual(self.user1.username, 'testuser')
        self.assertEqual(self.user1.id, self.user1_id)


    def test_user_model_following(self):
        """Tests model's following instance methods."""
        self.assertEqual(self.user3.is_following(self.user2), True)
        self.assertEqual(self.user3.is_followed_by(self.user2), False)
        self.assertEqual(self.user2.is_followed_by(self.user3), True)


    def test_user_model_signup(self):
        """Tests model's signup class method."""
        self.assertEqual(self.signup1, self.signup1)
        self.assertEqual(isinstance(self.signup1, User), True)


    def test_user_model_signup_with_existing_user(self):
        """Tests model's signup class method with exisitng credentials."""
        new_signup = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http//:www.testjpg.jpg"
        )
        self.assertRaises(IntegrityError, db.session.commit)


    def test_user_model_authenticate(self):
        """Tests model's authenticate class method."""
        usrnm = self.signup1.username
        signin = User.authenticate(usrnm, "HASHED_PASSWORDsignup")
        self.assertEqual(signin, self.signup1)

        
    def test_user_model_invalid_authenticate(self):
        """Tests model's authenticate class method with wrong credentials."""
        usrnm = self.signup1.username
        signin = User.authenticate(usrnm, "wrongpassword")
        self.assertEqual(signin, False)