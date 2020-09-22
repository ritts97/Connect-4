from mongoengine import *
from app.configuration.db import db

class Moves(db.Document):
    token = db.StringField(required=True, unique=True)
    matrix = db.BinaryField()
    moves = db.ListField()
    winner = db.StringField()