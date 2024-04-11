from flask import Blueprint, jsonify, render_template, request, flash, redirect
from flask_login import login_required, current_user
from . import db   ##means from __init__.py import db
from .models import Note, Food
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

# @views.route('/')
# @login_required #this code limit the only user who have logined can access.

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
     if request.method == 'POST':
          note = request.form.get('note')

          if len(note) < 1 :
               flash('Note is too short!', category='error')
          else:
               # new_note = Note(data=note)
               new_note = Note(data=note,user_id = current_user.id )

               db.session.add(new_note)
               db.session.commit()

               flash('Note added!', category='success')



     return render_template("home.html", user=current_user)
     # return render_template("home.html")

@views.route('/delete-note', methods=['POST'])
def delete_note():
     note = json.loads(request.data)
     noteId = note['noteId']
     note = Note.query.get(noteId)
     if note :
          if note.user_id == current_user.id: 
               db.session.delete(note)
               db.session.commit()
               return jsonify({})
          
# @views.route('/delete_food', methods=['POST'])
# def delete_food():
#      food = json.loads(request.data)
#      foodId = food['noteId']
#      food = Food.query.get(foodId)
#      if food :
#           if food.user_id == current_user.id: 
#                db.session.delete(food)
#                db.session.commit()
#                return jsonify({})
          
@views.route('/delete_food/<int:food_id>', methods=['POST'])
def delete_food(food_id):
    food = Food.query.get(food_id)
    if food:
        if food.user_id == current_user.id:
            db.session.delete(food)
            db.session.commit()
            return redirect(request.url), jsonify({'message': 'Food item deleted successfully'})
        else:
            return redirect(request.url), jsonify({'error': 'You are not authorized to delete this food item'}), 403
    else:
        return redirect(request.url), jsonify({'error': 'Food item not found'}), 404
    
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

     return render_template("food.html", food_dmm=food_dmm, user=current_user)

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

     return render_template("food_publish.html", food_dmm=food_dmm, user=current_user)




@views.route('/food_admin')
@login_required
def food_admin():
     note_dmm = Note.query.all()
     print( note_dmm[0].data )

     return render_template("food_admin.html", user=current_user,note_dmm=note_dmm)

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
               difficult_level = request.form.get('difficult_level')

               food_image_path = 'static/' + str(image.filename)
               print(food_image_path )
               new_food = Food(food_name = food_name,
                               food_raw = food_raw,
                               food_step = food_step ,
                               food_time=food_time,
                               food_image_path = food_image_path,
                               difficult_level = difficult_level,
                               user_id = current_user.id )
               db.session.add(new_food )
               db.session.commit()
               # login_user(new_user , remember=True)
               flash('Food added!', category='success')

               return redirect(request.url)
     


     return render_template("food_form.html", user=current_user)

