
class ZipCodeNotFound(RuntimeError):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class Backend(object):

	def __init__(self, config={}):
		pass
	
	def find(self, zipcode):
		raise ZipCodeNotFound(zipcode)

