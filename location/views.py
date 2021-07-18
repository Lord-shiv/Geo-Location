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

    # GEOPY
    geolocator = Nominatim(user_agent="location")
    ip = '209.95.50.14'
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)

    # location coordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # initial folium map

    if form.is_valid():
        instance = form.save(commit=False)
        d_destination = form.cleaned_data.get('destination')
        g_destination = geolocator.geocode(d_destination)

        # destination coordinates
        d_lat = g_destination.latitude
        d_lon = g_destination.longitude
        pointB = (d_lat, d_lon)

        # distance calculation
        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification
        instance.user_location = location
        instance.distance = distance
        instance.save()

    context = {
        'distance': obj,
        'form': form,
    }

    return render(request, 'location/test.html', context)
