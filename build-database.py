import csv

db = open('allCountries.txt', 'r')

r = csv.DictReader(db,  dialect=csv.Sniffer().sniff(db.read(1000)))

# Reset file pointer
db.seek(0)

for row in r:
  print row