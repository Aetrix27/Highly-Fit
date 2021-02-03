import jinja2
import os

from pprint import PrettyPrinter
from flask import Flask, request, render_template

################################################################################
## SETUP
################################################################################

app = Flask(__name__)

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('data'),
])
app.jinja_loader = my_loader

pp = PrettyPrinter(indent=4)

################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():

    return render_template('index.html') 

