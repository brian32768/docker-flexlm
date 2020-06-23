from flask import Flask
import flask_bootstrap
from flask_bootstrap import Bootstrap
from config import Config
import logging
# FIXME-- I don't know where logging output will go right now!

__VERSION__ = 'license_monitor 1.3'

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes


