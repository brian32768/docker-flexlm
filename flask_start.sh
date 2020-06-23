#!/usr/bin/bash
# This starts the flask app as a standalone on Windows

LMHOME='C:/Program Files (x86)/ArcGIS/LicenseManager/bin'
LMUTIL="lmutil.exe"
LICENSE="service.txt"

# I have no idea why my Windows Server instance needs the pwd here, freaky.
python `pwd`/start_app.py
