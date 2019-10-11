"""
Runs as a standalone webserver that checks status of the ArcGIS license server and returns an HTML page.

@author: Brian Wilson <bwilson@co.clatsop.or.us>
"""
from __future__ import print_function
import sys, os, subprocess
import re
from flask import Flask
from time import sleep

app = Flask(__name__)

# Set to True if We only care if all licenses are in use
SHOWLIMITONLY = True

def file_must_exist(f):
    if os.path.exists(f): return
    msg = f + " not found."
    try: 
        raise FileNotFoundError(msg)
    except:
        raise IOError(msg)

try:
    service_file = sys.argv[1]
except:
    service_file = 'service.txt'
    print("WARNING: Using default service file name")
file_must_exist(service_file)

try:
    lmutil = os.environ['LMUTIL']
    file_must_exist(lmutil)
    args = [lmutil, 'lmstat', '-c', service_file, '-a']
except KeyError:
    print("TEST MODE INVOKED: because no LMUTIL env variable.")
    lmutil = 'lmutil'
    args = ["cat", "lmstat.txt"]



#--- Okay, we have everything we need!

def generate_page():
    """ Generate the contents of a web page from lmutil. """

    # Create a pipe to talk to lmutil
    p = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)

    # Turn lmutil output into a web page 
    return process_licenses(p.stdout)

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
        #print(line)

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

    msg = '<html><body>\n<h1>ArcGIS License Server</h1>\n'

    msg += ("Product: <b>%s</b> License server version: <b>%s</b> <br />" % daemon_status)
    
    msg += ("<h3>Current License Usage</h3>\n")
    msg += ('<table border=1>\n')
    msg += ("<tr> <th>User</th> <th>Type</th> <th>Computer</th> <th>Start</th> </tr>\n")
    for user in sorted(userinfo):
        for info in userinfo[user]:
            (license_type, computer, start) = info
            msg += ("<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr>\n" % (user, license_type, computer, start))
    msg += ('</table>')

    if len(licenses) :
        if SHOWLIMITONLY:
            msg += "<h1>License limit reached!</h1>\n"
        else:
            msg += "<h3>Licenses on this server</h3>"

        msg += ('<table border=1>\n')
        msg += ("<tr> <th>Type</th> <th>Total</th> <th>In use</th> </tr>\n")
        for type in sorted(licenses):
            (issued, in_use) = licenses[type]
            if (issued <= in_use): 
                type   = '<em>%s</em>' % type
                in_use = '<em>%s</em>' % in_use
            msg += ("<tr> <td>%s</td> <td>%s</td> <td>%s</td> </tr>\n" % (type, issued, in_use))
        msg += ('</table>\n')

    msg += '</body></html>'
    return msg

@app.route('/')
def index():
    """ This is the web service """
    return generate_page()

def test_parser(test_file):
    # Test parsing under Visual Studio with this text file instead of lmstat!
    with open(test_file, 'r') as fp:
        msg = process_licenses(fp)
        print(msg)

if __name__ == '__main__':

    #test_parser('lmstat.txt')
    #exit(0)

    print("Test run, to confirm everything works before starting server.")
    print(generate_page())

    print("Starting service.")
    app.run(host = '0.0.0.0', debug = False)

# That's all!
