import csv

db = open('US/US.txt', 'r')

r = csv.DictReader(db,  dialect=csv.Sniffer().sniff(db.read(1000)))

# Reset file pointer
db.seek(1190000)

i = 0;

for row in r:
    print row
    y = 0
    # print row.keys()
    # print row.values()

    i = i + 1
    if ( i > 99 ):
        break