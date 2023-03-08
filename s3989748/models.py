from flask_sqlalchemy import SQLAlchemy
import logging as lg

from .views import app

# Create database connection object
db = SQLAlchemy(app)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, username, password):
        self.email    = email
        self.username = username
        self.password = password

db.create_all()

def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    lg.warning('Database initialized!')