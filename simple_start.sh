#!/usr/bin/bash
# This is a simple shell to start the standalone on Windows

LMHOME='C:/Program Files (x86)/ArcGIS/LicenseManager/bin'
LMUTIL="lmutil.exe"
LICENSE="service.txt"

python license_monitor.py
