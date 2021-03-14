# Authors: Antonia Ritter and Kai Johnson
# Adapted from app.py in tiny-webapp
# CS257 
# Feb-Mar 2021 

import sys
import argparse
import flask
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/<path:path>')
def shared_header_catchall(path):
    return flask.render_template(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Our world ag output webapp')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
