import requests
import json

# URL of the webhook
url = "http://localhost:5000/webhook"

# JSON data to be sent in the request body
operation_status_data = {
  "specversion": "1.0",
  "id": "1534ab08-967b-44de-a5aa-dd6af38da1ab",
  "type": "OperationalStatusChanged",
  "subject": "NLCON-1",
  "time": "2023-03-22T16:04:43.554626Z",
  "source": "https://pLonWeuShaResApi01.azure-api.net/v1/chargepoints",
  "datacontenttype": "application/json",
  "data": {
    "status": "Available",
    "chargepointid": "NLCON00000941",
    "connectornumber": 0,
    "evseid": 0,
    "statussource": "StatusNotification"
  }
}

userinput_data = {
    "userinputid": 1234,
    "subject": "NLCON-1",
    "endtime": "2023-03-22T16:04:43.554626Z",
    "demand": 20
}

session_data = {
  "specversion": "1.0",
  "id": "acc105a2-43d6-4a74-9d88-2e1e69c44a63",
  "type": "SessionUpdate",
  "subject": "NLCON-3",
  "time": "2023-03-22T16:19:52.5606119Z",
  "source": "https://pLonWeuShaResApi01.azure-api.net/v1/sessions",
  "datacontenttype": "application/json",
  "data": {
    "totalenergyinkwh": 2.665,
    "totalduration": "00:15:07.5606116",
    "totalcosts": 1.8325
  }
}

# Convert the data to JSON format
session_data = json.dumps(session_data)
userinput_data = json.dumps(userinput_data)
operation_status_data = json.dumps(operation_status_data)

# Set the headers for the request
headers = {
    "Content-Type": "application/json",
    "authentication": "test"
}

# Send the POST request
# while True:
response = requests.post(url, data=session_data, headers=headers)

# Check the status code of the response
if response.status_code == 200:
    print("Webhook successfully sent!")
else:
    print(f"Failed to send webhook: {response.status_code}")
