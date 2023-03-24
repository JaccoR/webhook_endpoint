import logging
from flask import Flask, request
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import threading

# Import variables from const.py
from const import MONGODB_URL, AUTH_KEY, DB_NAME, HTTP_BAD_REQUEST, HTTP_INTERNAL_SERVER_ERROR, HTTP_OK, HTTP_UNAUTHORIZED, COLLECTION_MAP

# Init Flask app
app = Flask(__name__)

# Initialize database variables
mongo_client = None
db = None
# Create a lock object
mongo_lock = threading.Lock()

# Set up logging
app.logger.setLevel(logging.INFO)

def check_environment_variables():
    # Check that required environment variables are set
    if not MONGODB_URL:
        app.logger.error("MongoDB URL not set")
        exit(1)

    if not AUTH_KEY:
        app.logger.error("Authentication key not set")
        exit(1)

def connect_to_mongodb():
    # Test connection with MongoDB
    global mongo_client, db
    try:
        mongo_client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000, maxPoolSize=50)
        mongo_client.server_info()
        db = mongo_client[DB_NAME]
        app.logger.info(f'Connected with MongoDB')
    except ServerSelectionTimeoutError as e:
        app.logger.error(f"Error connecting to MongoDB: {e}")
        exit(1)

def get_collection(data):
    # Check for a similar key between the COLLECTION_MAP and the data and use this to identify the correct collection
    # Find the first common key
    common_key = None
    collection_map_keys = COLLECTION_MAP.keys()
    for key in collection_map_keys:
        if key in data:
            common_key = key
            break
    
    # Use this common key to return the correct collection
    if common_key is not None:
        collection = COLLECTION_MAP.get(common_key)
        return collection
    else:
        app.logger.warning(f"Data seems in a different format and does not contain fields: {collection_map_keys}, skipping")
        return None
    
def put_data_in_mongodb(data, collection):
    # Try to put data in mongoDB
    try:
        # Acquire the lock before accessing the database
        mongo_lock.acquire()

        db[collection].insert_one(data)
        app.logger.info(f'Successfully inputted data into the {collection} collection')
        return True
    except Exception as e:
        app.logger.error(f"Error inserting data into MongoDB: {e}")
        return False
    finally:
        # Release the lock after accessing the database even when an exception is raised
        mongo_lock.release()
    
def parse_data(data):
    # Parse the JSON data from the request body and save to MongoDB
    try:
        return request.json
    except:
        app.logger.error(f"Error parsing data to JSON: {data}")
        return None


def process_webhook_data():
    # Authenticate the request
    if not authenticate_request(request):
        return 'Authentication failed', HTTP_UNAUTHORIZED
    
    # Parse the JSON data
    data = parse_data(request)

    # Validate json data
    if data is None:
        return 'Invalid data', HTTP_BAD_REQUEST
    
    collection = get_collection(data)

    # Validate the data
    if collection is None:
        return 'Invalid data', HTTP_BAD_REQUEST

    # Put data in mongodb
    success =  put_data_in_mongodb(data, collection)

    # Check if inputting data worked
    if not success:
        return 'Error', HTTP_INTERNAL_SERVER_ERROR

    # No premature errors so inputted data!
    return 'OK', HTTP_OK
    
def authenticate_request(request):
    # Check if the authentication key matches the expected value
    header_auth_key = request.headers.get('authentication')
    if header_auth_key != AUTH_KEY:
        app.logger.warning(f"Authentication failed: Invalid key: {header_auth_key} of address: {request.remote_addr}")
        return False
    return True

@app.route('/webhook', methods=['POST'])
def webhook():
    # The webhook endpoint itself
    response, status_code = process_webhook_data()
    return response, status_code



























