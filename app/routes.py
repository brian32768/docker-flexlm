from IPython.display import display
from flask import render_template, redirect, flash
from app import app
from config import Config

import sys, os, subprocess
import re
from flask import Flask
from time import sleep
from datetime import datetime, timezone
import pytz

app = Flask(__name__)

# Set to True if We only care if all licenses are in use
SHOWLIMITONLY = True

def render_page():
    """ Generate the contents of a web page from lmutil. """

    # Create a pipe to talk to lmutil
    p = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)

    # Turn lmutil output into a web page 
    form = process_licenses(p.stdout)
    return render_template('licenses.html', form=form)

def process_licenses(fp):

    # Define the regular expressions used to parse the output of lmstat.
    re_daemon = re.compile(r'\s*(\w+)\: UP (.*)')
    re_license_type = re.compile(r'^Users of (\S+):.* of (\d+).* of (\d+).*')
    re_user_info = re.compile(r'\s+(\S+)\s+(\S+).*start\s+(.*)')

    daemon_status = ('??product type not found','??')
    licenses = {}
    userinfo = {}

    for r in fp.readlines():
        line = r.rstrip().decode('utf-8')
        if not len(line): continue

        mo = re_daemon.search(line)
        if (mo):
            product_type = mo.group(1)
            version = mo.group(2)
            daemon_status = (product_type, version)
            continue

        mo = re_license_type.search(line)
        if (mo):
            license_type = mo.group(1)
            issued = mo.group(2)
            in_use = mo.group(3)
#            print(license_type, issued, in_use)
            if (SHOWLIMITONLY and (issued > in_use)):
                continue
            licenses[license_type] = (issued, in_use)
            continue

        mo = re_user_info.search(line)
        if (mo):
            user = mo.group(1)
            computer = mo.group(2)
            start = mo.group(3)

            info = (license_type, computer, start)
            if (user in userinfo):
                userinfo[user].append(info)
            else:
                userinfo[user] = [info]
#            print(license_type, user, computer, start)

    # When someone hits reload it's nice to see a change
    utc = datetime.now()
    tz  = pytz.timezone("America/Los_Angeles")
    form = {
        'time': str(tz.localize(utc)),
        'product': product,
        'version': daemon_status,
    }
        
#    for user in sorted(userinfo):
#        for info in userinfo[user]:
#            (license_type, computer, start) = info
#            msg += ("<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr>\n" % (user, license_type, computer, start))
#    msg += ('</table>')

#    if len(licenses) :
#        if SHOWLIMITONLY:
#            msg += "<h1>License limit reached!</h1>\n"
#        else:
#            msg += "<h3>Licenses on this server</h3>"

#        msg += ('<table border=1>\n')
#        msg += ("<tr> <th>Type</th> <th>Total</th> <th>In use</th> </tr>\n")
#        for type in sorted(licenses):
#            (issued, in_use) = licenses[type]
#            if (issued <= in_use): 
#                type   = '<em>%s</em>' % type
#                in_use = '<em>%s</em>' % in_use
#            msg += ("<tr> <td>%s</td> <td>%s</td> <td>%s</td> </tr>\n" % (type, issued, in_use))

    return form


def test_parser(test_file):
    # Test parsing with this text file instead of lmstat!
    with open(test_file, 'r') as fp:
        msg = process_licenses(fp)
        print(msg)

@app.route('/')
def main():
    return render_page()

# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    # UNIT TEST
    print(render_page())

# That's all!
