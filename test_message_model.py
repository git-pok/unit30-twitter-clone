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
        """
            Drop/create tables and delete queries.
            Create database data.
        """
        db.drop_all()
        db.create_all()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        self.client = app.test_client()
        
        u = User(
            id=1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=""
        )
        self.user = u
        id = u.id
        db.session.add(u)

        msg = Message(
            text="test text",
            user_id=id,
            timestamp=datetime.utcnow()
        )
        self.msg = msg
        db.session.add(msg)
        db.session.commit()
    
    def tearDown(self):
        """Tear down session data."""
        db.session.rollback()


    def test_message_model_relationship(self):
        """Tests model's relationships."""
        user_id = self.user.id
        self.assertEqual(len(self.msg.like), 0)
        self.assertEqual(self.msg.user, self.user)
        self.assertEqual(self.msg.id, user_id)
        self.assertEqual(self.msg.user.email, self.user.email)
        
    
    def test_message_model_instances(self):
        """Tests model's instances."""
        # Message object should have data
        user_id = self.user.id
        self.assertEqual(self.msg.text, "test text")
        self.assertEqual(isinstance(self.msg.timestamp, datetime), True)
