"""
SIMPLE VERSION

This runs as a standalone webserver that queries the ArcGIS
license server and returns a plain vanilla HTML page.
"""
import sys, os
from flask import Flask
from datetime import datetime
import pytz
from read_lmutil import ReadLmutil

app = Flask(__name__)

def generate_page(data_dict):
    """ Generate the contents of a web page from lmutil. """

    msg = '<html><body>\n'

    # When someone hits reload it's nice to see a change
    utc = datetime.now()
    tz  = pytz.timezone("America/Los_Angeles")
    pst = tz.localize(utc)
    msg += '<p>' + str(pst) + '</p>'
    
    msg += "Product: <b>%s</b> License server version: <b>%s</b> <br />" % (data_dict['vendor'], data_dict['version'])
    
    msg += ("<h3>Current License Usage</h3>\n")
    msg += ('<table border=1>\n')
    msg += ("<tr> <th>License</th> <th>Total</th> <th>In use</th> <th>Users</th> </tr>\n")

    for license in data_dict['licenses']:
        users = '<table>'
        total = license['total']
        in_use = license['in_use']
        for info in license['users']:
            users += '<tr><td>%s</td><td>%s</td><td>%s</tr>' % (
                info['name'], info['computer'], info['start'])
        users += '</table>'
        productname = license['productname']
        if in_use:
            # flag ALL LICENSES IN USE here by making them RED
            flag = 'green' if in_use < total else 'red'
            productname = '<font color="' + flag + '"><B>' + productname + '</B>'
        msg += '<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr>\n' % (productname,
                     license['total'], in_use, users)
    msg += ('</table>')

    msg += '</body></html>'
    return msg

@app.route('/')
def index():
    """ This is the web service """
    data_dict = ReadLmutil.read()
    return generate_page(data_dict)

if __name__ == '__main__':

    print("Test run, to confirm everything works before starting server.")
    data_dict = ReadLmutil.read()
    print(generate_page(data_dict))

    print("Starting service.")
    app.run(host = '0.0.0.0', debug = False)

# That's all!
