import time
import BaseHTTPServer
import urlparse
import json
import redis
import os
import time

from mixpanel import Mixpanel

HOST_NAME = 'localhost'
PORT_NUMBER = int(os.environ.get('ZIPTASTIC_PORT', 80))

class ZipAPIServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        # Hacky time analytics
        start_time = time.time()

        mp = Mixpanel("260efdc73003178a9c05ffb14f426483")
        
        # Get the zip from the data
        qs = {}
        path = s.path
        the_zip = None
        the_country = None
        old_db = True

        if path.startswith("/v2"):
            old_db = False
            path = path[3:]

        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            the_zip = qs.get('zip', [''])[0]
        elif path:
            the_zip = path.strip('/')

        p = path.lstrip("/")
        p = p.split("/", 2)

        if len(p) == 2:
            the_zip = p[1]
            the_country = p[0]

        if the_country is None:
            the_country = 'US'

        if the_country == 'CA':
            the_zip = the_zip[:3].upper()

        the_zip = the_zip.split('-')[0]

        if the_zip:
            # Query database with the ZIP and pull the city, state, country
            r = redis.StrictRedis(host='localhost', port=8322, db=0)

            if old_db:
                location = r.hgetall(the_zip)
            else:
                location = r.hgetall("{0}:{1}".format(the_country, the_zip))

            if len(location) > 0:
                s.send_response(200)
                s.send_header("Access-Control-Allow-Origin", "*")
                s.send_header("Content-type", "application/json")
                s.end_headers()
                s.wfile.write(json.dumps(location))
            else:
                s.send_response(404)
                s.send_header("Access-Control-Allow-Origin", "*")
                s.send_header("Content-type", "text/plain")
                s.end_headers()
                s.wfile.write("{}")
        else:
            s.send_response(400)
            s.send_header("Access-Control-Allow-Origin", "*")
            s.send_header("Content-type", "application/json")
            s.end_headers()
            s.wfile.write("{}")

        end_time = time.time()
        total_time = end_time-start_time
        if s.client_address[0] != '127.0.0.1':
            mp.track('Ziptastic', 'API Request', {'request-time': total_time, 'remote-ip': s.client_address[0] })

    def do_OPTIONS(s):
        s.send_response(200)
        s.send_header("Access-Control-Allow-Origin", "*")
        s.send_header("Access-Control-Allow-Headers", "X-Requested-With,X-Prototype-Version")
        s.end_headers()


def start_server():
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ZipAPIServerHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    start_server()
