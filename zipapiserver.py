import time
import BaseHTTPServer
import urlparse
import json
import sqlite3


HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80 # Maybe set this to 9000.

class ZipAPIServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        # Get the zip from the data
        qs = {}
        path = s.path
        the_zip = None
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            the_zip = qs['zip']
        elif path:
            the_zip = [path.strip('/').split('-')[0]]


        if the_zip:
            # Query database with the ZIP and pull the city, state, country
            conn = sqlite3.connect('zipcodes.db')
            c = conn.cursor()

            c.execute('select Country, State, City from zipcodes where ZipCode=?', the_zip)

            row = c.fetchone()
            if row is not None:
                s.send_response(200)
                # The Magic!
                s.send_header("Access-Control-Allow-Origin", "*")
                s.send_header("Content-type", "application/json")
                s.end_headers()
        
                data = dict(zip(('country', 'state', 'city'), row))
                s.wfile.write(json.dumps(data))
            else:
                # The Magic!
                s.send_response(404)
                s.send_header("Access-Control-Allow-Origin", "*")
                s.send_header("Content-type", "text/plain")
                s.end_headers()
                s.wfile.write("404 - Not Found")

    def do_OPTIONS(s):
        s.send_response(200)
        s.send_header("Access-Control-Allow-Origin", "*")
        s.send_header("Access-Control-Allow-Headers", "X-Requested-With,X-Prototype-Version")
        s.end_headers()


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ZipAPIServerHandler)
    #print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
