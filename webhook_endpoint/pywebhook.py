import logging
import os
from flask import Flask, request
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import threading

# Import variables from const.py
from const import MONGODB_URL, AUTH_KEY, DB_NAME, HTTP_BAD_REQUEST, HTTP_INTERNAL_SERVER_ERROR, HTTP_OK, HTTP_UNAUTHORIZED, COLLECTION_MAP, LOG_FORMAT, DATE_FORMAT

# Init Flask app
app = Flask(__name__)

# Initialize database variables
mongo_client = None
db = None
# Create a lock object
mongo_lock = threading.Lock()

# Set up logging
logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook_route():
    # Authenticate the request
    if not authenticate_request(request):
        return 'Authentication failed', HTTP_UNAUTHORIZED

    try:
        # Parse the JSON data
        data = parse_data(request)
    except ValueError as e:
        app.logger.error(f"Error parsing data to JSON: {e}")
        return 'Invalid data', HTTP_BAD_REQUEST

    collection = get_collection(data)

    if collection is None:
        return 'Invalid data', HTTP_BAD_REQUEST

    if not put_data_in_mongodb(data, collection):
        return 'Error', HTTP_INTERNAL_SERVER_ERROR

    return 'OK', HTTP_OK

def check_environment_variables():
    if not MONGODB_URL:
        app.logger.error("MongoDB URL not set")
        exit(1)

    if not AUTH_KEY:
        app.logger.error("Authentication key not set")
        exit(1)

def connect_to_mongodb():
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
    common_key = None
    collection_map_keys = COLLECTION_MAP.keys()
    for key in collection_map_keys:
        if key in data:
            common_key = key
            break
    
    if common_key is not None:
        collection = COLLECTION_MAP.get(common_key)
        return collection
    else:
        app.logger.warning(f"Data seems in a different format and does not contain fields: {collection_map_keys}, skipping")
        return None

def put_data_in_mongodb(data, collection):
    try:
        mongo_lock.acquire()
        db[collection].insert_one(data)
        app.logger.info(f'Successfully inputted data into the {collection} collection')
        return True
    except Exception as e:
        app.logger.error(f"Error inserting data into MongoDB: {e}")
        return False
    finally:
        mongo_lock.release()

def parse_data(request):
    return request.get_json()

def authenticate_request(request):
    header_auth_key = request.headers.get('authentication')
    if header_auth_key != AUTH_KEY:
        app.logger.warning(f"Authentication failed: Invalid key: {header_auth_key} of address: {request.remote_addr}")
        return False
    return True

