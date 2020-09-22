from flask import Flask
from app.configuration import db, config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config.DevConfig())
db.initialize_db(app)

@app.route("/")
def index():
    return "Welcome to Count4 game!"