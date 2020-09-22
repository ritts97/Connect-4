from flask import Flask, request, url_for, Response, jsonify, session
from app.configuration import db, config
from flask_mongoengine import MongoEngine
from app.models.Moves import Moves
from flask_cors import CORS
from uuid import uuid4
import numpy as np

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config.DevConfig())
CORS(app, resources={r"/*": {"origins": "*"}})
db.initialize_db(app)

@app.route("/")
def index():
    return "Welcome to Count4 game!"

@app.route('/start')
def start():
    try:
        body = request.data
        if body.decode('utf-8') == 'START':
            token = str(uuid4())
            session['token'] = token
            resp = {
                "token" : token,
                "message" : "READY"
            }
            return jsonify(resp)
    except Exception as e:
        return e