from django.db import models


class LocationMeasurement(models.Model):
    '''location model'''
    user_location = models.CharField(max_length=200)
    defined_destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Distance from {self.user_location} to {self.defined_destination} is {self.distance} km."
