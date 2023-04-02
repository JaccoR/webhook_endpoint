import requests
import json

# URL of the webhook
url = "http://localhost:5000/webhook"

# JSON data to be sent in the request body
data = {
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

# Convert the data to JSON format
json_data = json.dumps(data)

# Set the headers for the request
headers = {
    "Content-Type": "application/json",
    "authentication": "test"
}

# Send the POST request
# while True:
response = requests.post(url, data=json_data, headers=headers)

# Check the status code of the response
if response.status_code == 200:
    print("Webhook successfully sent!")
else:
    print(f"Failed to send webhook: {response.status_code}")
