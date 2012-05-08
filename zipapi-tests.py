import unittest
import urllib2
import zipapiserver


class TestPostalCodeAPI(unittest.TestCase):
	def setUp(self):
		pass
		#zipapiserver.start_server()

	def test_GET_variable_success(self):
		url = "http://localhost/?zip=48867"
		f = urllib2.urlopen(url)
		self.assertEqual(f.read(), '{"country": "US", "state": "MI", "city": "OWOSSO"}')

	def test_GET_variable_failure(self):
		url = "http://localhost/?zip=4886234237"
		try:
			f = urllib2.urlopen(url)
			self.fail
		except urllib2.HTTPError:
			pass

	def test_path_variable_success(self):
		url = "http://localhost/48867"
		f = urllib2.urlopen(url)
		self.assertEqual(f.read(), '{"country": "US", "state": "MI", "city": "OWOSSO"}')

	def test_path_variable_failure(self):
		url = "http://localhost/4886234237"
		try:
			f = urllib2.urlopen(url)
			self.fail
		except urllib2.HTTPError:
			pass

	def test_path_variable_with_country_success(self):
		url = "http://localhost/v2/US/48867"
		f = urllib2.urlopen(url)
		self.assertEqual(f.read(), '{"country": "US", "state": "Michigan", "city": "Owosso"}')

	def test_path_variable_with_country_failure(self):
		url = "http://localhost/v2/WEFG/4886234237"
		try:
			f = urllib2.urlopen(url)
			self.fail
		except urllib2.HTTPError:
			pass

if __name__ == '__main__':
    unittest.main()