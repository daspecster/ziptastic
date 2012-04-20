import json
import traceback
import sys

from ziptastic import ZipCodeNotFound

#from ziptastic.redis import Backend
from ziptastic.sqlite3 import Backend

backend = Backend()

def FourOhFour ( start_response ):
		start_response('404 NOT FOUND', [('content-type', 'text/plain')])
		return ('Not Found',)

def application(environ, start_response):
	if '/' != environ['PATH_INFO']:
		return FourOhFour( start_response )
	
	if 'GET' != environ['REQUEST_METHOD']:
		start_response('405 METHOD NOT ALLOWED', [('content-type', 'text/plain')])
		return ('Method Not Allowed',)

	if 'QUERY_STRING' not in environ:
		return FourOhFour( start_response )

	params = {}
	for param in environ['QUERY_STRING'].split('&'):
		pair = param.split('=')
		params[pair[0]] = pair[1] if ( 2 == len( pair ) ) else ""

	if 'zipcode' not in params:
		return FourOhFour( start_response )

	try:
		d = backend.find(int(params['zipcode']))
	except ZipCodeNotFound:
		return FourOhFour( start_response )
	except Exception, e:
		traceback.print_exc()
		start_response('500 INTERNAL SERVER ERROR', [('content-type', 'text/plain')])
		return ('Internal Server Error',)

	if 'callback' not in params or 0 == len( params['callback'] ):
		start_response('200 OK', [('content-type', 'application/json'),("Access-Control-Allow-Origin", "*")])
		return (json.dumps(d),)
	else:
		start_response('200 OK', [('content-type', 'text/javascript'),("Access-Control-Allow-Origin", "*")])
		return ( params['callback'] + '(' + json.dumps(d) + ');', )

