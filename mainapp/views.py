from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ReportedFires,Stations,Employee
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session


def index(request):
   
    return render(request, 'index.html')

from django.http import JsonResponse

@csrf_exempt
def report_fire(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phoneNumber')
        message = request.POST.get('message')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # You can process the data here (e.g., save it to a database)
        # Replace the following code with your own logic
        # For now, we'll just return a JSON response indicating success.
        reported_fire = ReportedFires(
            message=message,
            reporterTelNumber=phone_number,
            latitude=latitude,
            longitude=longitude,
        )
        reported_fire.save()

        '''response_data = {
            'status': 'success',
            'phone_number': phone_number,
            'message': message,
            'latitude': latitude,
            'longitude': longitude,
        }'''
        message = 'Fire reported successfully'

        return render(request, 'index.html', {'message': message})
    else:
        
        return render(request, 'index.html', {'message': 'Fire not reported successfully call our emergecy number'})

def login_page(request):
    return render (request,'login.html')

def official_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')

        # Check if there is an official with the given name and ID number
        try:
            official = Employee.objects.get(name=name, IdNumber=id_number, official=True)
            request.session['user_id'] = official.id

            # Get reported cases for the official's station
            reported_cases = ReportedFires.objects.filter(StationPlaced=official.station)
            #print(reported_cases)
            location = official.station.location
            print("location is ",location)


            return render(request, 'notifications.html', {'official': official, 'reported_cases': reported_cases,'location':location})
        except Employee.DoesNotExist:
            error_message = 'Wrong credentials. Please try again.'

        return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')





def confirm_fire(request, case_id):
    # Get the fire report by ID
    fire_report = get_object_or_404(ReportedFires, id=case_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'confirm':
            # Change the status to True (confirmed)
            fire_report.status = True
            fire_report.save()
    user_id = request.session['user_id']
    official = Employee.objects.get(id=user_id)
    reported_cases = ReportedFires.objects.filter(StationPlaced=official.station)
    location = official.station.location
    

    return render(request, 'notifications.html', {'official': official, 'reported_cases': reported_cases,'location':location})

   

def cancel_fire(request, case_id):
    # Get the fire report by ID
    fire_report = get_object_or_404(ReportedFires, id=case_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'cancel':
            # Delete the fire report
            fire_report.delete()

    # Redirect back to the page with updated information
    user_id = request.session['user_id']
    official = Employee.objects.get(id=user_id)
    reported_cases = ReportedFires.objects.filter(StationPlaced=official.station)
    location = official.station.location
    

    return render(request, 'notifications.html', {'official': official, 'reported_cases': reported_cases,'location':location})


def homepage(request):
    return render (request,'homepage.html')

from django.shortcuts import render
import folium
from folium.plugins import HeatMap

def heatmap(request):
    # Create a Folium map
    map_obj = folium.Map(location=[1.2921, 36.817223], zoom_start=6)
    data = [
    [-1.286389, 36.817223, 0.1],   # Nairobi
    [-4.043477, 39.668206, 0.1],   # Mombasa
    [-0.091702, 34.767956, 0.1],   # Kisumu
    [0.516667, 35.283333, 0.1],    # Eldoret
    [-0.283333, 36.066667, 0.1],   # Nakuru
    [-1.033333, 37.066667, 0.1],   # Thika
    [0.283333, 34.75, 0.1],        # Kakamega
    [-1.522778, 37.263056, 0.1],   # Machakos
    [0.061622, 37.648972, 0.1],    # Meru
    [-0.675833, 34.767222, 0.1]    # Kisii
]
    HeatMap(data).add_to(map_obj)

    # Save the map as an HTML file
    map_html = map_obj._repr_html_()

    # Pass the HTML content to the template for rendering
    return render(request, 'heatmap.html', {'map_html': map_html})

def preventitive(request):
    return render (request,'preventitive.html')

