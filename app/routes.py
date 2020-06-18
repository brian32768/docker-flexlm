from flask import Flask, render_template, redirect, flash
from config import Config

import sys, os, subprocess
import re
from time import sleep
from datetime import datetime, timezone

from app import app

@app.route('/')
def main_page():
    """ Generate the contents of a web page from lmutil. """

    # Create a pipe to talk to lmutil
    if Config.TEST_MODE:
        fp = open(Config.TEST_FILE, 'r', encoding="utf-8")
    else:
        p = subprocess.Popen(Config.LMUTIL, stdout=subprocess.PIPE, bufsize=1)
        fp = p.stdout

    utc = datetime.utcnow().replace(tzinfo=timezone.utc, second=0, microsecond=0)

    # Define the regular expressions used to parse the output of lmstat.
    re_daemon = re.compile(r'\s*(\w+)\: UP (.*)')
    re_license_type = re.compile(r'^Users of (\S+):.* of (\d+).* of (\d+).*')
    re_user_info = re.compile(r'\s+(\S+)\s+(\S+).*start\s+(.*)')

    product = "none at all"
    daemon_status = ('??product type not found','??')
    licenses = {}
    userinfo = {}

    for r in fp.readlines():
        line = r.rstrip()
        if not len(line):
            continue

        mo = re_daemon.search(line)
        if (mo):
            product_type = mo.group(1)
            version = mo.group(2)
            daemon_status = (product_type, version)
            continue

        mo = re_license_type.search(line)
        if (mo):
            license_type = mo.group(1)
            total = mo.group(2)
            in_use = mo.group(3)
            #print(license_type, total, in_use)
            licenses[license_type] = {'total':total, 'in_use':in_use}
            continue

        mo = re_user_info.search(line)
        if (mo):
            username = mo.group(1)
            info = {
                'name': username,
                'license_type':license_type, 
                'computer': mo.group(2), 
                'start': mo.group(3)
            }

            if (username in userinfo):
                userinfo[username].append(info)
            else:
                userinfo[username] = [info]
        pass

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

    fp.close()

    return render_template('licenses.html',
        timestamp = utc,
        product =  product,
        arcgis_version = daemon_status,
        licenses = licenses,
        userinfo = userinfo
    )   


# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    # UNIT TESTS
    test_parser(Config.TEST_FILE)
    print(main_page())

# That's all!
