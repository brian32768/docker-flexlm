from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
import logging
# FIXME-- I don't know where logging output will go right now!

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes

__VERSION__ = 'license_monitor 1.3'


