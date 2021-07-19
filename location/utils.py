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
        return 12
    elif distance > 100 and distance <= 500:
        return 7
    elif distance > 500 and distance <= 1200:
        return 6
    elif distance > 1200 and distance <= 1800:
        return 5
    elif distance > 1800 and distance <= 5000:
        return 4
    elif distance > 5000 and distance <= 12000:
        return 3
    else:
        return 2


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
