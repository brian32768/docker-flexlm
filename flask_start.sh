#!/usr/bin/bash
# This starts the flask app as a standalone on Windows

LMHOME='C:/Program Files (x86)/ArcGIS/LicenseManager/bin'
LMUTIL="lmutil.exe"
LICENSE="service.txt"

export LMHOME
export LMUTIL
export LICENSE

# Obviously this is not the right way to do this.
#PYTHON=/c/Users/bwilson.CLATSOP/AppData/Local/ESRI/conda/envs/arctic/python
PYTHON=python

# I have no idea why my Windows Server instance needs the pwd here, freaky.
$PYTHON `pwd`/start_app.py
