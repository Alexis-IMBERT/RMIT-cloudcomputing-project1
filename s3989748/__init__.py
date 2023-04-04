import os
from flask import Flask

from .views import app
from . import models


@app.cli.command()
def init_db():
    models.init_db()
