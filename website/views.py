from flask import Blueprint, jsonify, render_template, request, flash, redirect
from flask_login import login_required, current_user
from . import db   ##means from __init__.py import db
from .models import Note, Food, User, RatingMemory
import json
import os

# --------
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
DB_NAME = "database.db"
engine = create_engine(f'sqlite:///{DB_NAME}') 
Session = sessionmaker(bind=engine)
session = Session()
# --------


views = Blueprint('views',__name__)

def Find_username(id_input):
     all_users = User.query.all()
     for usr in all_users :
          if usr.id == id_input:
               print(usr.first_name)
               return usr.first_name


# @views.route('/')
# @login_required #this code limit the only user who have logined can access.
@views.route('/food', methods=['GET','POST'])
@login_required
def food():
     food_dmm = Food.query.all()
     
     # print( note_dmm[0].data )

     if request.method == 'POST':
          # search_term = request.form.get('search_term', None)
          search_term = request.form.get('search_term', None)
          print(search_term )
     # if search_term:
          food_dmm = Food.query.filter(Food.food_name.contains(search_term)).all()
     else:
          food_dmm = Food.query.all()

     if food_dmm:
          print(food_dmm [0].food_name) 
          print(food_dmm [0].food_image_path ) 

     return render_template("food.html", food_dmm=food_dmm, current_user=current_user, Find_username=Find_username,Is_rating=Is_rating, Count_rating=Count_rating )




@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
     food_dmm = Food.query.all()
     # print( note_dmm[0].data )

     if request.method == 'POST':
          # search_term = request.form.get('search_term', None)
          search_term = request.form.get('search_term', None)
          print(search_term )
     # if search_term:
          food_dmm = Food.query.filter(Food.food_name.contains(search_term)).all()
     else:
          food_dmm = Food.query.all()

     if food_dmm:
          print(food_dmm [0].food_name) 
          print(food_dmm [0].food_image_path ) 

     return render_template("food.html", food_dmm=food_dmm, current_user=current_user, Find_username=Find_username,Is_rating=Is_rating, Count_rating=Count_rating )


def Is_rating(food_id):
     status = False

     # Score_ = RatingMemory.query.get(food_id)
     all_Score_ = RatingMemory.query.all()

     # Accessing individual columns of each row
     user_dmm = []
     for score_ in all_Score_ :
          if score_.food_id == food_id :
               user_dmm.append(score_.user_id)

     my_list = list(set(user_dmm))
  
     for item in my_list:
          if item == current_user.id:
               status = True
     return status

def Count_rating(food_id):

          # Score_ = RatingMemory.query.get(food_id)
     all_Score_ = RatingMemory.query.all()

     # Accessing individual columns of each row
     user_dmm = []
     for score_ in all_Score_ :
          if score_.food_id == food_id :
               user_dmm.append(score_.user_id)

     my_list = list(set(user_dmm))
     return len( my_list )
          
@views.route('/rating/<int:food_id>', methods=['POST'])
@login_required
def rating(food_id):
#     class RatingMemory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     food_id = db.Column(db.Integer)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

     # Score_ = RatingMemory.query.all()
     print(" food_id is being rated : ", food_id)
     print(" user_id is rating : ",current_user.first_name)
     
     if not(Is_rating(food_id)):
          new_rating = RatingMemory(food_id  = food_id, user_id = current_user.id)
          db.session.add( new_rating )
          db.session.commit()
     

     # food_dmm = RatingMemory.query.filter(RatingMemory.user_id.contains(current_user.id)).all()
     # food_ = Food.query.all()
     food_ = Food.query.all()
     for food_pvt in food_:
          if food_pvt.id == food_id :
               food_name = food_pvt.food_name 

     # Score_ = RatingMemory.query.get(food_id)
     all_Score_ = RatingMemory.query.all()

     # Accessing individual columns of each row
     user_dmm = []
     for score_ in all_Score_ :
     # rating_id = rating.id
          if score_.food_id == food_id :
               # print("user id who have already rated (food id : ",food_id ,food_name,") is :",score_.user_id)
               user_dmm.append(score_.user_id)

     
     # flash( food_  , category='success')
     

     my_list = list(set(user_dmm))
     print("all users have rated : ", my_list )
     print("current_user.id :",current_user.id)
     search_item = current_user.id
     found = False
     for item in my_list:
          if item == search_item:
               check = True
     if check :
          pass
          # flash("rate แล้ว ", category='danger')
     else:
          flash('เมนู "' + str(food_name)+'" ได้รับคะแนน + 1 '+' จากคุณ ' + current_user.first_name, category='success')

               
     return redirect('/food')


@views.route('/delete_food/<int:food_id>', methods=['POST'])
@login_required
def delete_food(food_id):
     food = Food.query.get(food_id)
     if food:
          if food.user_id == current_user.id:
               db.session.delete(food)
               db.session.commit()
               flash('Food item deleted successfully', category='success')
               # return redirect('/food')
          else:
               flash('Food item deleted successfully', category='error')
               # return redirect('/food')
     else:
          flash('Food item deleted successfully', category='error')
          
     return redirect('/food')
    

@views.route('/food_publish', methods=['GET','POST'])
def food_publish():
     food_dmm = Food.query.all()

     if request.method == 'POST':
          # search_term = request.form.get('search_term', None)
          search_term = request.form.get('search_term', None)
          print(search_term )
     # if search_term:
          food_dmm = Food.query.filter(Food.food_name.contains(search_term)).all()
     else:
          food_dmm = Food.query.all()

     if food_dmm:
          print(food_dmm [0].food_name) 
          print(food_dmm [0].food_image_path ) 

     return render_template("food_publish.html", food_dmm=food_dmm, user=current_user, Find_username=Find_username,Is_rating=Is_rating, Count_rating=Count_rating )


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@views.route('/food_form', methods=['GET','POST'])
def food_form():
     target = os.path.join(APP_ROOT, 'static/')

     if request.method == 'POST':

          if request.files :

               image = request.files["image"]
               print(image)
               image.save(os.path.join(target, image.filename))
               image_path = os.path.join(target, image.filename)
               print("Image saved")
              

               food_name = request.form.get('food_name')
               food_raw = request.form.get('food_raw')
               food_step = request.form.get('food_step')
               food_time = request.form.get('food_time')
               food_rating = 0
               difficult_level = request.form.get('difficult_level')

               food_image_path = 'static/' + str(image.filename)
               print(food_image_path )
               new_food = Food(food_name = food_name,
                               food_raw = food_raw,
                               food_step = food_step ,
                               food_time=food_time,
                               food_image_path = food_image_path,
                               difficult_level = difficult_level,
                               user_id = current_user.id ,
                               food_rating = food_rating )
               db.session.add(new_food )
               db.session.commit()
               # login_user(new_user , remember=True)
               flash('Food added!', category='success')

               return redirect(request.url)
     


     return render_template("food_form.html", user=current_user)

