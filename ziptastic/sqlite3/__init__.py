import ziptastic 
import sqlite3

class Backend(ziptastic.Backend):

	def __init__(self, config={}):
		self.config = {'database': 'zipcodes.db'}
		self.config.update(config)
	
	def find( self, zipcode):
		conn = sqlite3.connect(self.config['database'])
		c = conn.cursor()
		c.execute('SELECT Country, State, City FROM zipcodes WHERE ZipCode=?', (str(zipcode),))

		row = c.fetchone()

		if not row:
			raise ziptastic.ZipCodeNotFound(zipcode)

		d = dict(zip(('country', 'state', 'city'), row))
		d['zipcode'] = zipcode

		return d

