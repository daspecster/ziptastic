import json
import redis
import os
import time

from datetime import timedelta
from functools import update_wrapper

from flask import Flask, Response, jsonify, abort, make_response, request, current_app
from mixpanel import Mixpanel

HOST_NAME = 'localhost'
PORT_NUMBER = int(os.environ.get('ZIPTASTIC_PORT', 80))

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    resp = jsonify({})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



@app.route("/3/<country>/<postal_code>", methods=['GET', 'HEAD', 'OPTIONS'])
@crossdomain(origin='*')
def ziptastic(country, postal_code):
    # Hacky time analytics
    start_time = time.time()

    mp = Mixpanel("260efdc73003178a9c05ffb14f426483")

    if country is None:
        tcountry = 'US'

    if country == 'CA':
        postal_code = postal_code[:3].upper()

    postal_code = postal_code.split('-')[0]

    if postal_code:
        # Query database with the ZIP and pull the city, state, country
        r = redis.StrictRedis(host='localhost', port=8322, db=0)

        location = r.lrange("{0}:{1}".format(country, postal_code), 0, -1)
        print location
        if len(location) > 0:
            resp = Response(json.dumps(location).decode('string_escape'),  mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'
        else:
            abort(404)

    end_time = time.time()
    total_time = end_time-start_time

    mp.track('Ziptastic', 'API Request', {
        'request-time': total_time,

    })

    return resp

if __name__ == "__main__":
    app.run(port=8321, debug=True)
