from pymongo import MongoClient

import csv
import sys

import geohash
"""
    <geohash>:<geonamid>
    sp91fgut91tx:9279724
"""

class GeonamesToMongoImport():

    # def add_to_index(self, lat, long, geonameid, r):
    #     """
    #     Adds the given point to the redis index.
    #     """

    #     # pid for Point ID
    #     pid = geohash.encode(lat, long)
    #     constituent = (pid[:i+1] for i in range(len(pid)))

    #     for area in constituent:
    #         print "MMA:" + area, geonameid
    #         # r.sadd("MMA:" + area, pid)
    #         r.sadd("MMA:" + area, geonameid)


    def build_database(self, filename):

        # For large CSV files, increase the size
        csv.field_size_limit(sys.maxsize)

        # connect to db
        mc = MongoClient()
        db = mc.ziptastic
        ziptastic_collection = db.ziptastic_codes

        with open(filename, 'rb') as txtdb:
            parseddb = csv.reader(txtdb, delimiter='\t')
            for row in parseddb:

                geonameid = row[0]
                name = row[1]
                asciiname = row[2]
                alternatenames   = row[3]
                latitude = row[4]
                longitude = row[5]
                feature_class = row[6]
                feature_code = row[7]
                country_code = row[8]
                cc2 = row[9]
                admin1_code = row[10]
                admin2_code = row[11]
                admin3_code = row[12]
                admin4_code = row[13]
                population = row[14]
                elevation = row[15]
                dem = row[16]
                timezone = row[17]
                modification_date = row[18] if len(row) > 18 else 'null'

                data = {
                            'geonameid': geonameid,
                            'name': name,
                            'asciiname': asciiname,
                            'alternatenames': alternatenames,
                            'latitude': latitude,
                            'longitude': longitude,
                            'feature_class': feature_class,
                            'feature_code': feature_code,
                            'country_code': country_code,
                            'cc2': cc2,
                            'admin1_code': admin1_code,
                            'admin2_code': admin2_code,
                            'admin3_code': admin3_code,
                            'admin4_code': admin4_code,
                            'population': population,
                            'elevation': elevation,
                            'dem': dem,
                            'timezone': timezone,
                            'modification_date': modification_date
                        }

                if country_code == 'US':
                    try:
                        ziptastic_collection.insert(data)
                    except:
                        pass
                    continue


                # self.add_to_index(float(latitude), float(longitude), geonameid, rgeohash)

if __name__ == '__main__':
    g = GeonamesToMongoImport()
    g.build_database('allCountriesData.txt')
