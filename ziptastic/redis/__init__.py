import ziptastic 
import redis

class Backend(ziptastic.Backend):

	def __init__(self, config={}):
		self.config = { 'host': 'localhost', 'port': 6379, 'db': 0, 'prefix': 'ziptastic:%d' }
		self.config.update(config)
		self.pool = redis.ConnectionPool(host=self.config['host'], port=self.config['port'], db=self.config['db'])

	def find(self, zipcode):
		r = redis.Redis(connection_pool=self.pool)
		key = self.config['prefix'] % zipcode
		d = r.hgetall(key)

		if 0 == len(d.keys()):
			raise ziptastic.ZipCodeNotFound(zipcode)
		
		d['zipcode'] = zipcode

		return d
