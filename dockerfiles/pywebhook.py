import logging
from flask import Flask, request
from pymongo import MongoClient

# Import variables from const.py
from const import MONGODB_URL, AUTH_KEY, DB_NAME, USER_INPUT_COLLECTION, LONGSHIP_COLLECTION, HTTP_BAD_REQUEST, HTTP_INTERNAL_SERVER_ERROR, HTTP_OK, HTTP_UNAUTHORIZED

# Init Flask app
app = Flask(__name__)

# Init DB variable so it is global
db = None

# Set up logging
app.logger.setLevel(logging.INFO)

# Connect to MongoDB
def connect_to_mongodb():
    try:
        global db
        mongo_client = MongoClient(MONGODB_URL)
        db = mongo_client[DB_NAME]
        app.logger.info(f'Connected with MongoDB')
        
    except Exception as e:
        app.logger.error(f"Error connecting to MongoDB: {e}, retrying max 5 times")
        exit(1)

# Check that required environment variables are set
def check_environment_variables():
    if not MONGODB_URL:
        app.logger.error("MongoDB URL not set")
        exit(1)

    if not AUTH_KEY:
        app.logger.error("Authentication key not set")
        exit(1)

# Save data to the appropriate MongoDB collection
def validate_and_send_to_mongodb(db):
    # Parse the JSON data from the request body and save to MongoDB
    try:
        data = request.json
    except:
        app.logger.error(f"Error parsing data to JSON: {data}")
        return 'Invalid data', HTTP_BAD_REQUEST
    
    # User Input set collection
    if "userinputid" in data:
        collection = USER_INPUT_COLLECTION
    # Longship set collection
    elif "longshipid" in data:
        collection = LONGSHIP_COLLECTION
    # Check invalid data
    else:
        app.logger.warning(f"Invalid data: {data}")
        return 'Invalid data', HTTP_BAD_REQUEST

    # Try to put data in mongoDB
    try:
        db[collection].insert_one(data)
        app.logger.info(f'Successfully inputted data into the {collection} collection')
        return 'OK', HTTP_OK
    except Exception as e:
        app.logger.error(f"Error inserting data into MongoDB: {e}")
        return 'Error', HTTP_INTERNAL_SERVER_ERROR
    
# Check if the authentication key matches the expected value
def authenticate(request):
    header_auth_key = request.headers.get('authentication')
    if header_auth_key != AUTH_KEY:
        app.logger.warning(f"Authentication failed: Invalid key: {header_auth_key} of address: {request.remote_addr}")
        return False
    return True
    
check_environment_variables()
connect_to_mongodb()

# Define the webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    # Authenticate the request
    if not authenticate(request):
        return 'Authentication failed', HTTP_UNAUTHORIZED

    response, status_code = validate_and_send_to_mongodb(db)

    return response, status_code



























