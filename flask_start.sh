#!/usr/bin/bash
# This starts the flask app as a standalone on Windows

LMHOME='C:/Program Files (x86)/ArcGIS/LicenseManager/bin'
LMUTIL="lmutil.exe"
LICENSE="service.txt"

python start_app.py
