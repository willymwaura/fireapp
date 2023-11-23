from django.db import models

# Create your models here.
from django.db import models

class Stations(models.Model):
    location = models.CharField(max_length=255)
    latitude = models.CharField(max_length=20)  # Change to CharField
    longitude = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.location

class ReportedFires(models.Model):
    message = models.TextField()
    reporterTelNumber = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20) # Change to CharField
    longitude = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    StationPlaced= models.ForeignKey(Stations, on_delete=models.CASCADE,null=True) # Default to True, but can be changed

    def __str__(self):
        return f"Reported Fire {self.id}"
    

    

class Employee(models.Model):
    name = models.CharField(max_length=255)
    TelNumber = models.CharField(max_length=20)
    official = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    station = models.ForeignKey(Stations, on_delete=models.CASCADE)
    IdNumber=models.CharField(max_length=20)

    def __str__(self):
        return self.name
