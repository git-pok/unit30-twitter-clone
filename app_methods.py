# Created everything in this file.
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash
import requests
from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, User, Message, Follows, Likes

def update_user(form_data, userf):
    """updates User instance and updates database"""
    userf.email = form_data.get("email") if form_data.get("email") != "" else userf.email
    userf.username = form_data.get("username") if form_data.get("username") != "" else userf.username
    userf.image_url = form_data.get("image_url") if form_data.get("image_url") != "" else userf.image_url 
    userf.header_image_url = form_data.get("header_image_url") if form_data.get("header_image_url") != "" else userf.header_image_url
    db.session.add(userf)
    db.session.commit()


def delete_like(message):
    """
    deletes row from Like model and table
    """
    Likes.query.filter_by(message_id=message).delete()
    db.session.commit()


def add_to_like(curr_user_id, liked_message_id, like_exists, message_user_id):
    if curr_user_id == message_user_id:
        flash("Current user cant like own messages.", "danger")
    elif like_exists:
        delete_like(liked_message_id)
        db.session.rollback()
        flash(f"Successfully unliked message!", "success")
    else:
        like = Likes(user_id=curr_user_id, message_id=liked_message_id)
        db.session.add(like)
        db.session.commit()
        db.session.rollback()
        flash(f"Successfully liked message!", "success")


def xml_check_for_header_img(user):
    """
    Checks if default header image is xml or a file path.
    Requests the image to see if its valid.
    Returns a status code.
    """
    if user.header_image_url != '/static/images/warbler-hero.jpg':
        image_request = requests.get(user.header_image_url)
        image_res_status_code = image_request.status_code
        return image_res_status_code
    else:
        return 400 
