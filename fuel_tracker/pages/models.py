from django.db import models


class Fuel(models.Model):
    car= models.CharField(max_length=100)
    fuel_date = models.DateField()
    fuel_firm = models.CharField(max_length=100)
    fuel_volume = models.FloatField()
    fuel_cost = models.FloatField()
    car_km = models.FloatField()

    def __str__(self):
        return f'{self.car} - {self.fuel_date}'
# Create your models here.
