import sqlite3
import redis

prefix = 'ziptastic:%d'
r = redis.Redis()

conn = sqlite3.connect('zipcodes.db')
c = conn.cursor()

for row in c.execute('SELECT zipcode, city, state, country FROM zipcodes'):
	r.hmset( prefix % row[0], { 'city': row[1], 'state': row[2], 'country': row[3] } )

