"""
When testing, you can start me with

    FLASK_APP=start_app flask run

"""
import sys
import os
from app import create_app
from version import version

app = create_app(os.environ.get('FLASK_ENV', 'default'))
