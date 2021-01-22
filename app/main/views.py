import sys, os, subprocess
import re
from time import sleep
from datetime import datetime, timezone, timedelta

from flask import Blueprint, render_template, redirect, flash
from flask import current_app

from . import main
from .read_lmutil import ReadLmutil


@main.route('/')
def main_page():
    """ Generate the contents of a web page from lmutil. """

    # System locale has to be set for this to work correctly.
    local = datetime.now().replace(microsecond=0)

    lmutil = ReadLmutil(current_app.config['LMUTIL'])
    data_dict = {'vendor': 'NONE', 'version':'0', 'licenses':[]}
    try:
        data_dict = lmutil.read()
    except Exception as e:
        print("Can't get data", e)

    return render_template('licenses.html',
        timestamp = local,
        product =  data_dict['vendor'],
        arcgis_version = data_dict['version'],
        licenses = data_dict['licenses'],
    )

# That's all!
