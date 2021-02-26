import jinja2
import os
from pymongo import MongoClient
import json
from bson import json_util
from pprint import PrettyPrinter
from flask import Flask, request, render_template, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


################################################################################
## SETUP
################################################################################



app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/workoutdatabase') + "?retryWrites=false"
app.config["MONGO_URI"] = host
mongo = PyMongo(app)


################################################################################
## ROUTES
################################################################################

@app.route('/model', methods=['GET'])
def show_model():
    return render_template('model.html')

@app.route('/workouts')
def get_workouts():
    workouts_data = mongo.db.workouts_data.find({})
    context = {
        'workouts': workouts_data
    }
    

    
    return render_template('workout.html', **context) 


@app.route('/createworkout', methods=["GET", "POST"])
def create():
    workout = request.form.get('workout_name')

    if request.method == 'POST':
    
        new_workout = {
            'workout_name' : workout
        }
       
        result=mongo.db.workouts_data.insert_one(new_workout)
        inserted_id = result.inserted_id

        return redirect(url_for('detail', workout_id=inserted_id))

    else:
        return render_template('createworkout.html')

@app.route('/workout/<workout_id>')
def detail(workout_id):
    workout_to_show = mongo.db.workouts_data.find_one({
        '_id': ObjectId(workout_id)
    })
    context = {
        'workout_id': ObjectId(workout_id),
        'workout': workout_to_show
    }
    return render_template('detail.html', **context)

@app.route('/edit/<workout_id>', methods=["GET", "POST"])
def edit(workout_id):
    if request.method == "POST":
        workout = request.form.get('workout_name')

        mongo.db.workouts_data.update_one({
            '_id': ObjectId(workout_id),
            
        },
        {
            '$set': {
                '_id': ObjectId(workout_id),
                'workout_name': workout
            }
        })

        return redirect(url_for('detail', workout_id=workout_id))
    else:

        workout_to_show=mongo.db.workouts_data.find_one({
            '_id': ObjectId(workout_id)
        })

        context = {
            'workout': workout_to_show
        }

        return render_template('edit.html', **context)
    
@app.route('/delete/<workout_id>', methods=['POST'])
def delete(workout_id):
    mongo.db.workouts_data.delete_one({
        '_id': ObjectId(workout_id)
    })
    
    return redirect(url_for('detail', workout_id=workout_id))
       

if __name__ == "__main__":
    app.run(debug=True)