import requests
import json

# URL of the webhook
url = "http://localhost:5000/webhook"

# JSON data to be sent in the request body
data = {
    "message": "Hello, World!",
    "timestamp": "2023-03-21T12:00:00Z",
    "userinputid": "tst"
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Set the headers for the request
headers = {
    "Content-Type": "application/json",
    "authentication": "test"
}

# Send the POST request
response = requests.post(url, data=json_data, headers=headers)

# Check the status code of the response
if response.status_code == 200:
    print("Webhook successfully sent!")
else:
    print("Failed to send webhook.")
