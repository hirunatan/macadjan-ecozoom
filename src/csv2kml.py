#!/usr/bin/env python
# encoding: utf-8

import os.path
import csv
import sys
import re
import math
import urllib2


def csv_to_kml(csv_file, kml_file):
    reader = csv.DictReader(csv_file, delimiter=',')

    kml_file.write(kml_start())

    for csv_row in reader:
        kml_file.write(kml_item(csv_row))

    kml_file.write(kml_end())

    csv_file.close()
    kml_file.close()


def kml_start():
    return """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
"""


def kml_item(csv_row):
    lat, lon = str_to_latlon(csv_row['Coordenadas'])
    return """
        <Placemark>
            <name><![CDATA[ {name}]]></name>
            <description><![CDATA[ <b><a href="https://15mpedia.org/wiki/{slug}">{name}</a></b><br/><p>{description}</p>]]></description>
            <Point>
                <coordinates>{coordinates}</coordinates>
            </Point>
        </Placemark>
""".format(
    name = csv_row[''],
    slug = csv_row[''].replace(' ', '_'),
    description = csv_row['Descripción'],
    coordinates = '{},{}'.format(lon, lat) if lon and lat else '',
)


def kml_end():
    return """
    </Document>
</kml>
"""


def str_to_latlon(latlon_str):
    '''
    Example latlon 42° 21' 12" N, 3° 40' 9" O
    '''
    match = re.match('''(\d+)° (\d+)' (\d+)" ([NS]), (\d+)° (\d+)' (\d+)" ([EO])''', latlon_str)
    if not match:
        return None, None

    lat_deg = int(match.group(1))
    lat_min = int(match.group(2))
    lat_sec = int(match.group(3))
    lat_orient = match.group(4)

    lon_deg = int(match.group(5))
    lon_min = int(match.group(6))
    lon_sec = int(match.group(7))
    lon_orient = match.group(8)

    lat = lat_deg + lat_min / 60.0 + lat_sec / 3600.0
    lon = lon_deg + lon_min / 60.0 + lon_sec / 3600.0

    if lat_orient == 'S':
        lat = -lat
    if lon_orient == 'O':
        lon = -lon

    return lat, lon


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print "Uso: csv2kml <url-fichero-csv> <ruta-fichero-kml>"
        exit(1)

    if sys.argv[1].lower().startswith("http"):
        csv_file = urllib2.urlopen(sys.argv[1])
    else:
        csv_file = open(sys.argv[1], 'rb')

    kml_file = open(sys.argv[2], 'w')

    csv_to_kml(csv_file, kml_file)

