import jinja2
import os
import pymongo

from pprint import PrettyPrinter
from flask import Flask, request, render_template
from flask_pymongo import PyMongo

################################################################################
## SETUP
################################################################################

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


@app.route('/model')
def model():
        
        return render_template('model.html') 

@app.route('/workout')
def workout():
        workout = 'abs'
        time_length = 200
        difficulty = 'beginner'
        equipment = 'weights'
        description = 'Do 3 reps'

        context = {
            'workout' : workout,
            'time_length': time_length,
            'difficulty': difficulty,
            'equipment': equipment,
            'description': description
        }

        return render_template('workout.html', **context) 
       

if __name__ == "__main__":
    app.run(debug=True)