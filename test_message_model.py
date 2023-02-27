"""Message model tests."""
# Added everything in this file.
# run these tests like:
# FLASK_ENV=production python -m unittest <name-of-python-file>
# python -m unittest test_user_model.py

import os
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

class MessageModelTestCase(TestCase):
    """Test Message model."""

    def setUp(self):
        """Drop/create tables and delete queries."""
        db.drop_all()
        db.create_all()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def tearDown(self):
        """Tear down session data."""
        db.session.rollback()


    def test_message_model_relationship(self):
        """Tests model's relationships."""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        id = u.id

        msg = Message(
            text="test text",
            user_id=id,
            timestamp=datetime.utcnow()
        )

        db.session.add(msg)
        db.session.commit()

        # Message should have no likes, and a user object
        self.assertEqual(len(msg.like), 0)
        self.assertEqual(msg.user, u)
        self.assertEqual(msg.id, 1)
        
    
    def test_message_model_instances(self):
        """Tests model's instances."""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        id = u.id

        msg = Message(
            text="test text",
            user_id=id,
            timestamp=datetime.utcnow()
        )

        db.session.add(msg)
        db.session.commit()

        # Message object should have data
        self.assertEqual(msg, msg)
        self.assertEqual(msg.text, 'test text')
        self.assertEqual(msg.id, 1)