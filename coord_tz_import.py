import redis
import csv
import sys

import geohash
"""
    <geohash>:<geonamid>
    sp91fgut91tx:9279724
"""

class GeonamesToRedisImport():

    def add_to_index(self, lat, long, timezone, r):
        """
        Adds the given point to the redis index.
        """

        # pid for Point ID
        pid = geohash.encode(lat, long)
        constituent = (pid[:i+1] for i in range(len(pid)))
        
        for area in constituent:
            # print "GH:" + pid, timezone
            # r.sadd("MMA:" + area, pid)
            r.hmset("GH:" + pid, { 'timezone': timezone })


    def build_database(self, filename):

        # For large CSV files, increase the size
        csv.field_size_limit(sys.maxsize)

        # connect to db
        # r = redis.StrictRedis(host='localhost', port=6379, db=0)
        rgeohash = redis.Redis(host='localhost', port=6379, db=1)

        counter = 0
        with open(filename, 'rb') as txtdb:
            parseddb = csv.reader(txtdb, delimiter='\t')
            for row in parseddb:
                
                if counter % 1000 == 0:
                    print counter
                
                geonameid = row[0]
                latitude = row[4]
                longitude = row[5]
                admin1_code_fips = row[10]
                timezone = row[17]

                counter = counter + 1
                
                # r.hmset(
                #     geonameid,
                #     {
                #         'latitude': latitude,
                #         'longitude': longitude,
                #         'admin1_code': admin1_code,
                #         'timezone': timezone
                #     }
                # )

                self.add_to_index(float(latitude), float(longitude), timezone, rgeohash)

if __name__ == '__main__':
    g = GeonamesToRedisImport()
    g.build_database('allCountriesData.txt')