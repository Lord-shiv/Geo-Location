# Helper
from typing import Counter
from django.contrib.gis.geoip2 import GeoIP2


def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon


def get_center_coordinates(latA, longA, latB=None, longB=None):
    cord = (latA, longA)

    if latB:
        cord = [(latA + latB)/2, (longA+longB)/2]
    return cord


def get_zoom(distance):
    if distance <= 100:
        return 11
    elif distance > 100 and distance <= 500:
        return 8
    else:
        return 2
