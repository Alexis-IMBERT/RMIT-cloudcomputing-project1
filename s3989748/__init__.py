import os
from flask import Flask

from .views import app
from . import models
from .models import db


@app.cli.command()
def init_db():
    models.init_db()
