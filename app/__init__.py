from flask import Flask
from app.configuration import db, config
from flask_mongoengine import MongoEngine
from app.models.Moves import Moves
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config.DevConfig())
CORS(app, resources={r"/*": {"origins": "*"}})
db.initialize_db(app)

@app.route("/")
def index():
    return "Welcome to Count4 game!"