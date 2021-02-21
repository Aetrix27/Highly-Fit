import jinja2
import os
from pymongo import MongoClient
import json
from bson import json_util
from pprint import PrettyPrinter
from flask import Flask, request, render_template
from flask_pymongo import PyMongo

################################################################################
## SETUP
################################################################################

cluster = MongoClient('mongodb+srv://johndoe:Hello123@cluster0.h18wa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = cluster['highlyfit']
collection = db['workouts']


app = Flask(__name__)

# host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/highly-fit') + "?retryWrites=false"
# app.config["MONGO_URI"] = host
# mongo = PyMongo(app)


# my_loader = jinja2.ChoiceLoader([
#     app.jinja_loader,
#     jinja2.FileSystemLoader('data'),
# ])
# app.jinja_loader = my_loader
# mongo = PyMongo(app)

# pp = PrettyPrinter(indent=4)

################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
        welcome = 'welcome to the '


        context = {
            'welcome': welcome
        }
        

        return render_template('index.html', **context) 

@app.route('/workout', methods=['GET'])
def get_workouts():
    all_workouts = list(collection.find({}))
    return json.dumps(all_workouts, default = json_util.default)
# return render_template('workout.html', **context) 

@app.route('/createworkout', methods=["GET", "POST"])
def create():

    if request.method == 'POST':
        # TODO: Get the new plant's name, variety, photo, & date planted, and 
        # store them in the object below.
        new_workout = {
            'workout_name': request.form.get('workout_name'),
        }
        # TODO: Make an `insert_one` database call to insert the object into the
        # database's `plants` collection, and get its inserted id. Pass the 
        # inserted id into the redirect call below.
        db.session.add('new_workout')
        db.session.commit()

        return redirect(url_for('detail', workout_id=new_workout.id))

    else:
        return render_template('createworkout.html')

       

if __name__ == "__main__":
    app.run(debug=True)