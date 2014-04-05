import json
import redis
import os
import time

from datetime import timedelta
from functools import update_wrapper

from flask import Flask, Response, jsonify, abort, make_response, request, current_app, g
from mixpanel import Mixpanel

HOST_NAME = 'localhost'
PORT_NUMBER = int(os.environ.get('ZIPTASTIC_PORT', 80))

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    resp = jsonify({})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.after_request
def inject_x_rate_headers(response):
    limit = get_view_rate_limit()
    if limit and limit.send_x_headers:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response


class RateLimit(object):
    expiration_window = 10

    def __init__(self, key_prefix, limit, per, send_x_headers):
        self.reset = (int(time.time()) // per) * per + per
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.per = per
        self.send_x_headers = send_x_headers
        tr = redis.StrictRedis(host='localhost', port=6379, db=0)
        p = tr.pipeline()
        p.incr(self.key)
        p.expireat(self.key, self.returneset + self.expiration_window)
        self.current = min(p.execute()[0], limit)

    remaining = property(lambda x: x.limit - x.current)
    over_limit = property(lambda x: x.current >= x.limit)

def get_view_rate_limit():
    return getattr(g, '_view_rate_limit', None)

def on_over_limit(limit):
    return 'You hit the rate limit', 400

def ratelimit(limit, per=300, send_x_headers=True,
              over_limit=on_over_limit,
              scope_func=lambda: request.remote_addr,
              key_func=lambda: request.endpoint):
    def decorator(f):
        def rate_limited(*args, **kwargs):
            key = 'rate-limit/%s/%s/' % (key_func(), scope_func())
            rlimit = ratelimit(key, limit, per, send_x_headers)
            g._view_rate_limit = rlimit
            if over_limit is not None and rlimit.over_limit:
                return over_limit(rlimit)
            return f(*args, **kwargs)
        return update_wrapper(rate_limited, f)
    return decorator

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
@ratelimit(limit=300, per=60 * 15)
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
