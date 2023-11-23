from django.db.models.signals import post_save
from django.dispatch import receiver
from mainapp.models import ReportedFires, Stations,Employee
from geopy.distance import great_circle
import json
import requests
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=ReportedFires)
def find_closest_station(sender, instance, created, **kwargs):
    if created and instance.latitude and instance.longitude:
        print(instance.latitude)
        print(instance.longitude)
        fire_latitude = float(instance.latitude)
        fire_longitude = float(instance.longitude)

        # Get all station coordinates
        stations = Stations.objects.all()

        # Calculate travel times from the fire location to each station
        closest_station = None
        min_distance = float('inf')

        for station in stations:
            station_latitude = float(station.latitude)
            station_longitude = float(station.longitude)

            # Calculate the distance using great-circle distance
            distance = great_circle((fire_latitude, fire_longitude), (station_latitude, station_longitude)).kilometers

            if distance < min_distance:
                min_distance = distance
                closest_station = station

        # Update the instance with the closest station
        instance.StationPlaced= closest_station
        instance.save()

        # Send SMS to officials of the closest station
        send_sms_to_officials(closest_station)

def send_sms_to_officials(station):
    try:
        official_employees = Employee.objects.filter(official=True, status=True, station=station)
        tel_numbers = [str(employee.TelNumber) for employee in official_employees]
        formatted_tel_numbers = ["254" + str(int(float(tel.strip()))) for tel in tel_numbers]

        now = timezone.now() + timedelta(hours=3)

        url = 'https://portal.zettatel.com/SMSApi/send'
        text = f'DEAR OFFICIAL,\nA fire has been reported at {now.strftime("%B %d, %Y %H:%M")} and placed to your station since its  the closest.\nPlease go to the admin page and confirm the fire immediately.'

        for formatted_tel_number in formatted_tel_numbers:
            print(formatted_tel_number)
            payload = {
                "userid": "Willy",
                "password": "GX98BFfh",
                "senderid": "KINYATHENA",
                "msgType": "text",
                "duplicatecheck": "true",
                "sendMethod": "quick",
                "sms": [{"mobile": [formatted_tel_number], "msg": text}]
            }

            json_payload = json.dumps(payload)
            headers = {'Content-Type': 'application/json'}

            response = requests.post(url, headers=headers, data=json_payload, timeout=10)

            # Check for successful response
            if response.status_code == 200:
                print(f"SMS sent successfully to {formatted_tel_number}")
            else:
                print(f"Failed to send SMS. Response status code: {response.status_code}, Response content: {response.text}")

    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
@receiver(post_save, sender=ReportedFires)
def send_fire_notification(sender, instance, created, **kwargs):
    print("the signal is running")
    # Check if the fire status has changed to True
    if instance.status and not created:
        # Get the station for the reported fire
        station = instance.StationPlaced

        # Get all members of the station
        station_members = Employee.objects.filter(station=station)
        print(station_members)

        # Compose the SMS message with a dynamic Google Maps link
        message = (
            f"Dear station members, a fire has been reported now. "
            f"Please take action immediately. "
            f"View the location on Google Maps: "
            f"https://www.google.com/maps/dir/?api=1&destination={instance.latitude},{instance.longitude}&travelmode=driving"
        )
        now = timezone.now() + timedelta(hours=3)

        url = 'https://portal.zettatel.com/SMSApi/send'

        
        # Send the SMS to all station members
        for member in station_members:
        
            # Replace the first number with '254'
            tel_no = member.TelNumber
            print(tel_no)
            if tel_no.startswith('0'):
                tel_no = '254' + tel_no[1:]
                print(tel_no)
                

            try:
                print("sending the sms")
                payload = {
                    "userid": "Willy",
                    "password": "GX98BFfh",
                    "senderid": "KINYATHENA",
                    "msgType": "text",
                    "duplicatecheck": "true",
                    "sendMethod": "quick",
                    "sms": [{"mobile": [tel_no], "msg": message}]
                }

                json_payload = json.dumps(payload)

                headers = {'Content-Type': 'application/json'}

                response = requests.post(url, headers=headers, data=json_payload)
                #print("API Response:", response.status_code, response.text)
            except Exception as e:
                print(f"Error sending SMS: {str(e)}")



        



