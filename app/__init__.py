import os
import logging
from flask import Flask, render_template
from config import config
from .extensions import *

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

bootstrap = Bootstrap()
debug_toolbar = DebugToolbarExtension()


def page_not_found(error):
    return render_template('404.html'), 404


def create_app(config_name='default'):
    """
    A flask application factory
    Arguments:
        config_name: key for the config dict
    """
    app = Flask(__name__)

    config_obj = config[config_name]
    app.config.from_object(config_obj)
    config_obj.init_app(app)

    bootstrap.init_app(app)
    debug_toolbar.init_app(app)

    # Add routes and custom error pages
     
    # Load blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Generic error handler
    app.register_error_handler(404, page_not_found)
    return app



