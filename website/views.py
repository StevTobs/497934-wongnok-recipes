from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from . import db   ##means from __init__.py import db
from .models import Note
import json

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
          
@views.route('/food')
@login_required
def food():
     return render_template("food.html", user=current_user)
          
