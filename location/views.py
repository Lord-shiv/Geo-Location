from django.shortcuts import get_object_or_404, render
# locals
from . models import LocationMeasurement
from . forms import LocationMeasurementForm
from . utils import get_geo
# geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def calculate_distance_view(request):
    obj = LocationMeasurement.objects.get(id=1)
    form = LocationMeasurementForm(request.POST or None)

    # geopy
    geolocator = Nominatim(user_agent="location")
    ip = '209.95.50.14'
    country, city, lat, lon = get_geo(ip)
    print('location country', country)
    print('location city', city)
    print('location lat lon', lat, lon)

    # will give is name of city from the ip address
    location = geolocator.geocode(city)
    print('location :::==>>', location)

    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    if form.is_valid():
        instance = form.save(commit=False)
        d_destination = form.cleaned_data.get('destination')
        g_destination = geolocator.geocode(d_destination)
        print(g_destination)
        d_lat = g_destination.latitude
        d_lon = g_destination.longitude

        pointB = (d_lat, d_lon)
        distance = round(geodesic(pointA, pointB).km, 2)

        instance.user_location = location
        instance.distance = distance
        instance.save()

    context = {
        'distance': obj,
        'form': form,
    }

    return render(request, 'location/test.html', context)


def home(request):
    return render(request, 'location/test.html')
