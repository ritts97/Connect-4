from flask import Flask, request, url_for, Response, jsonify, session
from app.configuration import db, config
from flask_mongoengine import MongoEngine
from app.utilities.errors import InternalServerError
from app.models.Moves import Moves
from flask_cors import CORS
from uuid import uuid4
import numpy as np
from bson.binary import Binary
import pickle

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config.DevConfig())
CORS(app, resources={r"/*": {"origins": "*"}})
db.initialize_db(app)

ROW_COUNT = 6
COL_COUNT = 7

def createConnectMatrix():
    matrix = np.zeros((ROW_COUNT, COL_COUNT))
    return matrix

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
            matrix = createConnectMatrix()
            serialisedBinaryMatrix = Binary(pickle.dumps(matrix, protocol=2), subtype=128)
            Moves(
                token = token,
                matrix = serialisedBinaryMatrix
            ).save()
            resp = {
                "token" : token,
                "message" : "READY"
            }
            return jsonify(resp)
        else:
            return "Invalid keyword! To start the game, send START"
    except Exception as e:
        raise InternalServerError