from django.urls import path
from . views import calculate_distance_view

app_name = "location"

urlpatterns = [
    path('calculate/', calculate_distance_view, name='calculate_distace_view'),
]
