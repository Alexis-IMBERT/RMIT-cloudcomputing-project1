import logging as lg

from .views import app

# Create database connection object


class Login(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # num_id = 0

    def __init__(self, email, username, password):
        # Login.num_id += 1
        # self.id       = Login.num_id
        self.email = email
        self.username = username
        self.password = password


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Login("s39897480@student.rmit.edu.au",
                       "AlexisIMBERT0", "AlexisIMBERT0"))
        db.session.commit()
        lg.warning('Database initialized!')
