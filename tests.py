import unittest
import urllib2
import zipapiserver
from zipapiserver import PORT_NUMBER


class TestPostalCodeAPI(unittest.TestCase):
	def setUp(self):
		pass

	def test_GET_variable_success(self):
		url = "http://localhost:{0}/?zip=48867".format(PORT_NUMBER)
		f = urllib2.urlopen(url)
		self.assertEqual(f.read(), '{"city": "OWOSSO", "state": "MI", "country": "US"}')

	def test_GET_variable_failure(self):
		url = "http://localhost:{0}/?zip=4886234237".format(PORT_NUMBER)
		try:
			f = urllib2.urlopen(url)
			self.fail
		except urllib2.HTTPError:
			pass

	def test_path_variable_success(self):
		url = "http://localhost:{0}/48867".format(PORT_NUMBER)
		f = urllib2.urlopen(url)
		self.assertEqual(f.read(), '{"city": "OWOSSO", "state": "MI", "country": "US"}')

	def test_path_variable_failure(self):
		url = "http://localhost:{0}/4886234237".format(PORT_NUMBER)
		try:
			f = urllib2.urlopen(url)
			self.fail
		except urllib2.HTTPError:
			pass

	def test_path_variable_with_country_success(self):
		url = "http://localhost:{0}/v2/US/48867".format(PORT_NUMBER)
		f = urllib2.urlopen(url)
		self.assertEqual(f.read(), '{"city": "Owosso", "state": "Michigan", "country": "US"}')

	def test_path_variable_with_country_failure(self):
		url = "http://localhost:{0}/v2/WEFG/4886234237".format(PORT_NUMBER)
		try:
			f = urllib2.urlopen(url)
			self.fail
		except urllib2.HTTPError:
			pass

if __name__ == '__main__':
    unittest.main()
