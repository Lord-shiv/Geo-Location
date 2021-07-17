from django.forms.fields import Field
from location.models import LocationMeasurement
from django import forms


class LocationMeasurementForm(forms.ModelForm):
    class Meta:
        model = LocationMeasurement
        fields = ('defined_destination', )
