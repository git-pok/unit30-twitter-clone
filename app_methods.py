from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash
from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, User, Message, Follows, Likes

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

# def add_to_like(user_idf, message_id, message_user_id):
#     if user_idf != message_user_id:
#         like = Likes(user_id=user_idf, message_id=message_idf)
#         db.session.add(like)
#         db.session.commit()
#         flash(f"Successfully liked message!", "success")
#     else:
#         flash("Current user cant like own messages.", "danger")

def delete_like(message):
    """
    deletes row from Like model and table
    """
    print('delete_like**************', message)
    Likes.query.filter_by(message_id=message).delete()
    db.session.commit()

def add_to_like(user_idf, message_idf, like_id, message_user_id):
    if user_idf == message_user_id:
        flash("Current user cant like own messages.", "danger")
    elif like_id:
        delete_like(message_idf)
        db.session.rollback()
        flash(f"Successfully unliked message!", "success")
    else:
        like = Likes(user_id=user_idf, message_id=message_idf)
        db.session.add(like)
        db.session.commit()
        db.session.rollback()
        flash(f"Successfully liked message!", "success")
