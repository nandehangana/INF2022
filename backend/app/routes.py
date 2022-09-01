from app import main
from flask import request, render_template, Response
from flask_cors import CORS
import json

app = main.app

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/', methods=['GET'])
@app.route('/home')
def home_page():
    return("Shark🦈!")





