import time
import BaseHTTPServer
import urlparse
import json
import sqlite3


HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80 # Maybe set this to 9000.

class ZipAPIServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        # The Magic!
        s.send_header("Access-Control-Allow-Origin", "*")
        s.end_headers()

        # Get the zip from the data
        qs = {}
        path = s.path
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            the_zip = qs['zip']

            # Query database with the ZIP and pull the city, state, country
            conn = sqlite3.connect('zipcodes.db')
            c = conn.cursor()

            c.execute('select Country, State, City from zipcodes where ZipCode=?', the_zip)

            row = c.fetchone()
            if row is not None:
                data = dict(zip(('country', 'state', 'city'), row))
                s.wfile.write(json.dumps(data))
            else:
                s.wfile.write("404")


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ZipAPIServerHandler)
    #print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
