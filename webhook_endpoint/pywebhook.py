
from flask import Flask, request

import threading

# Import variables from const.py
from const import AUTH_KEY, HTTP_BAD_REQUEST, HTTP_INTERNAL_SERVER_ERROR, HTTP_OK, HTTP_UNAUTHORIZED, COLLECTION_MAP

# Init Flask app
app = Flask(__name__)

# Create a lock object for thread-safety
mongo_lock = threading.Lock()

@app.route('/webhook', methods=['POST'])
def webhook_route():
    # Take the database from flask app
    db = app.config['db']
    # Authenticate the request
    if not authenticate_request(request):
        return 'Authentication failed', HTTP_UNAUTHORIZED

    try:
        # Parse the JSON data
        data = parse_data(request)
    except ValueError as e:
        app.logger.error(f"Error parsing data to JSON: {e}")
        return 'Invalid data', HTTP_BAD_REQUEST
    
    # If a certain key is in the data, present it via an api
    if "key" in data:
        # Present data in api endpoint
        return 'OK', HTTP_OK

    # Put data in mongoDB
    collection = get_collection(data)

    if collection is None:
        return 'Invalid data', HTTP_BAD_REQUEST

    if not put_data_in_mongodb(db, data, collection):
        return 'Error', HTTP_INTERNAL_SERVER_ERROR

    return 'OK', HTTP_OK

# Get the corresponding MongoDB collection based on the data content
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

# Insert data into the MongoDB collection
def put_data_in_mongodb(db, data, collection):
    try:
        # Acquire the lock for thread-safety
        mongo_lock.acquire()
        db[collection].insert_one(data)
        app.logger.info(f'Successfully inputted data into the {collection} collection')
        return True
    except Exception as e:
        app.logger.error(f"Error inserting data into MongoDB: {e}")
        return False
    finally:
        # Release the lock after accessing the database
        mongo_lock.release()

# Parse the JSON data from the request
def parse_data(request):
    return request.get_json()

# Authenticate the request based on the authentication key
def authenticate_request(request):
    header_auth_key = request.headers.get('authentication')
    if header_auth_key != AUTH_KEY:
        app.logger.warning(f"Authentication failed: Invalid key: {header_auth_key} of address: {request.remote_addr}")
        return False
    return True

