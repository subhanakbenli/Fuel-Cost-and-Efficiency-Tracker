from django.db import models
from django.contrib.auth.models import User



class Car(models.Model):
    car_name = models.CharField(max_length=100)
    car_brand = models.CharField(max_length=100, null=True, blank=True)
    car_model = models.CharField(max_length=100, null=True, blank=True)
    car_volume = models.FloatField(null=True, blank=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User tracking

    def __str__(self):
        return self.car_name

class Fuel(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    fuel_date  = models.DateField()
    fuel_firm = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=100)
    fuel_volume = models.FloatField()
    fuel_cost = models.FloatField()
    car_km = models.FloatField()

    def __str__(self):
        return f'{self.car} - {self.fuel_date}'
# Create your models here.

