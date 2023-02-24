from flask_sqlalchemy import SQLAlchemy
# from flask import flash, session
from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, User, Message, Follows

def update_user(userf, emailf, usernamef, image_urlf, header_image_urlf):
    """updates User instance and updates database"""
    if image_urlf and header_image_urlf: 
        userf.email = emailf
        userf.username = usernamef 
        userf.image_url = image_urlf 
        userf.header_image_url = header_image_urlf 
 
        db.session.add(userf)
        db.session.commit()
    if image_urlf and not header_image_urlf:
        userf.email = emailf
        userf.username = usernamef 
        userf.image_url = image_urlf 
        userf.header_image_url = userf.header_image_url 
 
        db.session.add(userf)
        db.session.commit()
    elif not image_urlf and header_image_urlf:
        userf.email = emailf
        userf.username = usernamef 
        userf.image_url = userf.image_url 
        userf.header_image_url = header_image_urlf 
 
        db.session.add(userf)
        db.session.commit()
    else:
        userf.email = emailf
        userf.username = usernamef 
        userf.image_url = userf.image_url 
        userf.header_image_url = userf.header_image_url 
 
        db.session.add(userf)
        db.session.commit()