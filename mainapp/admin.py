from django.contrib import admin
from mainapp.models import ReportedFires,Employee,Stations

# Register your models here.
admin.site.register(ReportedFires)
admin.site.register(Employee)
admin.site.register(Stations)
