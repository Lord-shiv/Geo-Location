# Helper
from typing import Counter
from django.contrib.gis.geoip2 import GeoIP2


def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon
