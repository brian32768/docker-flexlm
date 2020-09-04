from flask import Flask, render_template, redirect, flash
from config import Config

import sys, os, subprocess
import re
from time import sleep
from datetime import datetime, timezone, timedelta

from read_lmutil import ReadLmutil

from app import app

@app.route('/')
def main_page():
    """ Generate the contents of a web page from lmutil. """

    # System locale has to be set for this to work correctly.
    local = datetime.now().replace(microsecond=0)

    data_dict = ReadLmutil.read()

    return render_template('licenses.html',
        timestamp = local,
        product =  data_dict['vendor'],
        arcgis_version = data_dict['version'],
        licenses = data_dict['licenses'],
    )

# ------------------------------------------------------------------------

if __name__ == '__main__':    
    # UNIT TESTS
    pass

# That's all!
