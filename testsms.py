import requests
import json
#a script for sending sms in python

url = 'https://portal.zettatel.com/SMSApi/send'
'''
tel_no=112100378
tel_no=int(tel_no)
tel_no = "254{}".format(tel_no)'''
list_of_tel=['254112100378','254717291065','254745030446','254111560781','254713156754']

destination = "-1.0416410659467394,37.078626178942386"  # Use the reported fire location
travel_mode = "driving"
message = (
            f"Dear station members, a fire has been reported now. "
            f"Please take action immediately. "
            f"View the location on Google Maps: "
            f"https://www.google.com/maps/dir/?api=1&destination={destination}&travelmode={travel_mode}"
        )
for tel_no in list_of_tel:
# Define the JSON payload as a Python dictionary
    payload = {
        "userid": "Willy",
        "password": "GX98BFfh",
        "senderid": "ZTSMS",
        "msgType": "text",
        "duplicatecheck": "true",
        "sendMethod": "quick",
        "sms": [
            {
                "mobile": [tel_no],
                "msg": message
            }
    
        ]
    }

    # Convert the payload to a JSON string
    json_payload = json.dumps(payload)

    # Set the headers
    headers = {'Content-Type': 'application/json'}

    # Make the request
    response = requests.post(url, headers=headers, data=json_payload)

    # Print the response status code and content
    print(response.status_code)
    print(response.content)