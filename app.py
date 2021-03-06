import jinja2
import os
from pymongo import MongoClient
import json
from bson import json_util
from pprint import PrettyPrinter
from flask import Flask, request, render_template, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

################################################################################
## SETUP
################################################################################

app = Flask(__name__)
secret=os.getenv('VAR')

#Attempted to upload to Heroku using secret, if line doesnt work use host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/workoutdatabase') + "?retryWrites=false"
host = os.environ.get('MONGODB_URI', secret) + "?retryWrites=false"
app.config["MONGO_URI"] = host
mongo = PyMongo(app)

################################################################################
## ROUTES
################################################################################

@app.route('/', methods=['GET'])
def Launch_page():
    return render_template('index.html')
    
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


################################################################################
## LEG WORKOUTS
################################################################################
@app.route('/leg_workouts')
def leg_workouts():

    leg_workouts = mongo.db.workouts_data.find({
        'body_part' : 'legs'
    })
    context = {
        'workouts': leg_workouts
    }
    
    return render_template('leg_workouts.html', **context) 


################################################################################
## BACK WORKOUTS 
################################################################################

@app.route('/back_workouts')
def back_workouts():

    back_workouts = mongo.db.workouts_data.find({
        'body_part' : 'back'
    })
    context = {
        'workouts': back_workouts
    }
    
    return render_template('back_workouts.html', **context) 


################################################################################
## ABS WORKOUTS 
################################################################################
@app.route('/abs_workouts')
def abs_workouts():

    abs_workouts = mongo.db.workouts_data.find({
        'body_part' : 'abs'
    })
    context = {
        'workouts': abs_workouts
    }
    
    return render_template('abs_workouts.html', **context) 

################################################################################
## CHEST WORKOUTS 
################################################################################
@app.route('/chest_workouts')
def chest_workouts():

    chest_workouts = mongo.db.workouts_data.find({
        'body_part' : 'chest'
    })
    context = {
        'workouts': chest_workouts
    }
    
    return render_template('chest_workouts.html', **context) 

################################################################################
## ARM WORKOUTS 
################################################################################
@app.route('/arm_workouts')
def arm_workouts():

    arm_workouts = mongo.db.workouts_data.find({
        'body_part' : 'arms'
    })
    context = {
        'workouts': arm_workouts
    }
    
    return render_template('arm_workouts.html', **context) 

@app.route('/createworkout', methods=["GET", "POST"])
def create():
    workout = request.form.get('workout_name')
    workout_description = request.form.get('workout_description')
    body_part = request.form.get('body_part')
    workout_difficulty = request.form.get('workout_difficulty')

    if request.method == 'POST':
        new_workout = {
            'workout_name' : workout,
            'workout_description' : workout_description,
            'body_part': body_part,
            'workout_difficulty': workout_difficulty
    
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
        workout_description = request.form.get('workout_description')
        body_part = request.form.get('body_part')
        workout_difficulty = request.form.get('workout_difficulty')
        

        mongo.db.workouts_data.update_one({
            '_id': ObjectId(workout_id),
            
        },
        {
            '$set': {
                '_id': ObjectId(workout_id),
                'workout_name' : workout,
                'workout_description' : workout_description,
                'body_part': body_part,
                'workout_difficulty': workout_difficulty
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
