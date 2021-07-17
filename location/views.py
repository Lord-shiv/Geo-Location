from django.shortcuts import get_object_or_404, render
from . models import LocationMeasurement
from . forms import LocationMeasurementForm

# Create your views here.


def calculate_distance_view(request):
    return render(request)
