import os

SECRET_KEY = "\x0b<3R3O+f!PU-O Xi;J9n;:\\"

# Database initialization
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')