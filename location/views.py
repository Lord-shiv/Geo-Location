from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
# locals
from . models import LocationMeasurement
from . forms import LocationMeasurementForm
from . utils import get_geo, get_center_coordinates, get_zoom, get_ip
# geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# folium
import folium


def calculate_distance_view(request):
    '''calculate distance between two location'''
    distance = None
    destination = None
    form = LocationMeasurementForm(request.POST or None)
    # Geopy
    geolocator = Nominatim(user_agent="location")

    ip_ = get_ip(request)
    print(ip_)
    ip = '169.54.70.214'
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
        folium.Marker([l_lat, l_lon], popup=city['city'],
                      ).add_to(m)

        # destination marker
        folium.Marker([d_lat, d_lon], popup=destination,
                      ).add_to(m)

        # Line (draw) between two locations
        line = folium.PolyLine(
            locations=[pointA, pointB], weight=2, color='orange')
        m.add_child(line)

        instance.user_location = location
        instance.distance = distance
        instance.save()

    # check if modal is not poping
    # distance = None

    m = m._repr_html_()

    context = {
        'distance': distance,
        'form': form,
        'map': m,
        'destination': destination
    }

    return render(request, 'location/main.html', context)
