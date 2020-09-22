from flask import Flask
from app.configuration import db, config
from flask_mongoengine import MongoEngine
from app.models.Moves import Moves

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config.DevConfig())
db.initialize_db(app)

@app.route("/")
def index():
    Moves(
        token = "1232434"
    ).save()
    return "Welcome to Count4 game!"