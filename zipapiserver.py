import time
import BaseHTTPServer
import urlparse
import json
import sqlite3
import os

HOST_NAME = 'localhost'

if 'ZIPTASTIC_PORT' in os.environ:
    PORT_NUMBER = int(os.environ['ZIPTASTIC_PORT'])
else:
    PORT_NUMBER = 80

class ZipAPIServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        # Get the zip from the data
        qs = {}
        path = s.path
        the_zip = None
        the_country = None
        database_name = "zipcodes-old.db"

        if path.startswith("/v2"):
            database_name = "zipcodes.db"
            path = path[3:]

        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            the_zip = qs['zip'][0]
        elif path:
            the_zip = path.strip('/')
        
        p = path.lstrip("/")
        p = p.split("/", 2)

        if len(p) == 2:
            the_zip = p[1]
            the_country = p[0]

        the_zip = [the_zip.split('-')[0]]

        if the_zip:
            # Query database with the ZIP and pull the city, state, country
            conn = sqlite3.connect(database_name)
            c = conn.cursor()
            c.execute("SELECT Country, State, City from zipcodes WHERE zipcode LIKE ?", the_zip)

            row = c.fetchone()

            if row is not None:
                s.send_response(200)
                s.send_header("Access-Control-Allow-Origin", "*")
                s.send_header("Content-type", "application/json")
                s.end_headers()

                data = {'country': str(row[0]),'state': str(row[1]), 'city': str(row[2])}

                s.wfile.write(json.dumps(data))
            else:
                s.send_response(404)
                s.send_header("Access-Control-Allow-Origin", "*")
                s.send_header("Content-type", "text/plain")
                s.end_headers()
                s.wfile.write("{}")

    def do_OPTIONS(s):
        s.send_response(200)
        s.send_header("Access-Control-Allow-Origin", "*")
        s.send_header("Access-Control-Allow-Headers", "X-Requested-With,X-Prototype-Version")
        s.end_headers()


def start_server():
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ZipAPIServerHandler)
    #print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    start_server()