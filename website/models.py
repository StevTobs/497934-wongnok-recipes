from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(10000))
    food_raw = db.Column(db.String(10000))
    food_step = db.Column(db.String(10000))
    food_time = db.Column(db.Integer)
    food_image_path = db.Column(db.String(10000))  # Add this line for food_image_path column
    difficult_level = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
# class Food(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     food_name = db.Column(db.String(10000))
#     food_raw = db.Column(db.String(10000))
#     food_step= db.Column(db.String(10000))
#     food_time= db.Column(db.Integer)
#     food_image_path = db.Column(db.String(10000))
#     difficult_level = db.Column(db.Integer)
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    foods = db.relationship('Food')