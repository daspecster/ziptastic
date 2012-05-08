import sys
import csv
import sqlite3
import thread   

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

file_len('allCountries.txt') / 2

conn = sqlite3.connect("zipcodes.db")
c = conn.cursor()

c.execute('''create table if not exists zipcodes (id integer primary key, zipcode text, city text, state text, country text)''')


zipAdapter = csv.reader(open('allCountries.txt', 'rb'), delimiter="\t")

csv.field_size_limit(sys.maxint)

for row in zipAdapter:
    try:
        c.execute(u"insert into zipcodes values(NULL, ?, ?, ?, ?)",(buffer(row[1]), buffer(row[2]), buffer(row[3]), buffer(row[0])))
    except Exception as e:
    	print e.message
    	break
    conn.commit()
c.close()