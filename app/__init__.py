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

def makeMove(matrix, row, col, move):
    matrix[row][col] = move

def isValidMove(matrix, col):
    if col < 0 or col >= COL_COUNT:
        return False
    return matrix[ROW_COUNT - 1][col] == 0

def getValidRow(matrix, col):
    for i in range(ROW_COUNT):
        if matrix[i][col] == 0:
            return i

def isWinning(matrix, move):
    for i in range(COL_COUNT - 3):
        for j in range(ROW_COUNT):
            if matrix[j][i] == move and matrix[j][i+1] == move and matrix[j][i+2] == move and matrix[j][i+3] == move:
                return True
    for i in range(COL_COUNT):
        for j in range(ROW_COUNT - 3):
            if matrix[j][i] == move and matrix[j+1][i] == move and matrix[j+2][i] == move and matrix[j+3][i] == move:
                return True
    for i in range(COL_COUNT - 3):
        for j in range(ROW_COUNT - 3):
            if matrix[j][i] == move and matrix[j+1][i+1] == move and matrix[j+2][i+2] == move and matrix[j+3][i+3] == move:
                return True
    for i in range(COL_COUNT - 3):
        for j in range(3, ROW_COUNT):
            if matrix[j][i] == move and matrix[j-1][i+1] == move and matrix[j-2][i+2] == move and matrix[j-3][i+3] == move:
                return True

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
    except KeyError:
        raise KeyError
    except Exception as e:
        raise InternalServerError

@app.route('/makemoves')
def getMoves():
    try:
        body = request.get_json(force = True)
        token = body['token']
        if(token == session['token']):
            field = Moves.objects.get(token = token)
            col = int(body['col'])
            while field['gameValid']:
                matrix = pickle.loads(field['matrix'])
                if isValidMove(matrix, col):
                    row = getValidRow(matrix, col)
                    if field['turn'] == 1:
                        makeMove(matrix, row, col, 1)
                        field.modify(matrix = Binary(pickle.dumps(matrix, protocol=2), subtype=128), turn = 2)
                        field.moves.append({"Player":"Yellow", "Col":col})
                        field.save()
                        if isWinning(matrix, 1):
                            field.modify(gameValid = False, winner = "Yellow")
                            field.save()
                            return "Yellow wins!"
                        else:
                            return "Yellow made a move"

                    else:
                        makeMove(matrix, row, col, 2)
                        field.modify(matrix = Binary(pickle.dumps(matrix, protocol=2), subtype=128), turn = 1)
                        field.moves.append({"Player":"Red", "Col":col})
                        field.save()
                        if isWinning(matrix, 2):
                            field.modify(gameValid = False, winner = "Yellow")
                            field.save()
                            return "Red wins!" 
                        else:
                            return "Red made a move"
                else:
                    return "Invalid move!"
    except Exception as e:
        raise InternalServerError

@app.route('/getmoves')
def getMoveInfo():
    try:
        body = request.get_json(force=True)
        token = body['token']
        if token == session['token']:
            field = Moves.objects.get(token = token)
            return jsonify(field['moves'])
    except KeyError:
        raise KeyError
    except Exception as e:
        raise InternalServerError