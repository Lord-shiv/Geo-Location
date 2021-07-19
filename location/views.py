from django.shortcuts import get_object_or_404, render
# locals
from . models import LocationMeasurement
from . forms import LocationMeasurementForm
from . utils import get_geo, get_center_coordinates, get_zoom
# geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# folium
import folium


def calculate_distance_view(request):
    obj = LocationMeasurement.objects.get(id=1)
    form = LocationMeasurementForm(request.POST or None)

    # GEOPY
    geolocator = Nominatim(user_agent="location")
    ip = '72.46.131.10'
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)

    # Location coordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # Initial folium map
    m = folium.Map(width=1080, height=600,
                   location=get_center_coordinates(l_lat, l_lon), zoom_start=6)
    # location marker
    folium.Marker([l_lat, l_lon], popup=city['city'],
                  icon=folium.Icon(color='red')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('defined_destination')
        destination = geolocator.geocode(destination_)

        # Destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)

        # Distance calculation
        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification
        m = folium.Map(width=1080, height=640, location=get_center_coordinates(
            l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click me', popup=city['city'],
                      icon=folium.Icon(color='red')).add_to(m)

        # destination marker
        folium.Marker([d_lat, d_lon], tooltip='click me', popup=destination,
                      ).add_to(m)

        instance.user_location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

    context = {
        'distance': obj,
        'form': form,
        'map': m
    }

    return render(request, 'location/main.html', context)
