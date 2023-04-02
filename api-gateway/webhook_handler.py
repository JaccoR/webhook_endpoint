from flask import Flask, request
import threading
from const import AUTH_KEY, HTTP_BAD_REQUEST, HTTP_INTERNAL_SERVER_ERROR, HTTP_OK, HTTP_UNAUTHORIZED, COLLECTION_MAP, CHARGEPOINT_IDS, LONGSHIP_SESSION_STATUS_COLLECTION, LONGSHIP_SESSION_COLLECTION, USER_INPUT_COLLECTION

# Init Flask app
app = Flask(__name__)

# Create a lock object for thread-safety
mongo_lock = threading.Lock()

@app.route('/webhook', methods=['POST'])
def webhook_route():

    app.logger.debug(f"Received request with data: {request}")

    # Authenticate the request
    if not authenticate_request(request):
        return 'Authentication failed', HTTP_UNAUTHORIZED

    # Parse the JSON data
    webhook_data = parse_data(request)
    if not webhook_data:
        return 'Invalid data', HTTP_BAD_REQUEST

    # Check if data contains keys specversion (longship data) or userinput
    if not validate_data(webhook_data):
        return 'Invalid data', HTTP_BAD_REQUEST

    # Update the API when needed
    if check_and_update_api_data(webhook_data):
        return 'OK', HTTP_OK
    
    db = app.config['db']

    # Longship job session update
    if check_longship_session(webhook_data, db):
        return 'OK', HTTP_OK

    # User input
    if check_user_input(webhook_data, db):
        return 'OK', HTTP_OK

    return 'Error', HTTP_INTERNAL_SERVER_ERROR

# Insert data into the MongoDB collection
def put_data_in_mongodb(db, data, collection):
    try:
        # Acquire the lock for thread-safety using a context manager
        with mongo_lock:
            db[collection].insert_one(data)
            app.logger.info(f'Successfully inserted data into the {collection} collection')
            return True
    except Exception as e:
        app.logger.error(f"Error inserting data into MongoDB ({collection} collection): {e}")
        return False

# Parse the JSON data from the request
def parse_data(request):
    try:
        data = request.get_json()
        return data
    except ValueError as e:
        app.logger.error(f"Error parsing data to JSON: {e}")
        return None

# Authenticate the request based on the authentication key
def authenticate_request(request):
    header_auth_key = request.headers.get('authentication')
    if header_auth_key != AUTH_KEY:
        app.logger.warning(f"Authentication failed: Invalid key ({header_auth_key}) from address {request.remote_addr}")
        return False
    return True

def validate_data(webhook_data):
    if "specversion" not in webhook_data and "userinputid" not in webhook_data:
        app.logger.warning("Invalid data: missing key")
        return False
    if webhook_data["subject"] not in CHARGEPOINT_IDS:
        app.logger.debug(f"Invalid data: subject '{webhook_data['subject']}' not in allowed chargepoint IDs")
        return False
    return True

def check_and_update_api_data(webhook_data):
    if "type" in webhook_data and webhook_data["type"] == "OperationalStatusChanged":
        app.logger.info(f"Received OperationalStatusChanged, processing...")
        try:
            # Acquire the lock for thread-safety using a context manager
            with mongo_lock:
                chargepoint_collection = app.config['db'][LONGSHIP_SESSION_STATUS_COLLECTION]
                chargepoint_collection.update_one(
                    {'subject': webhook_data["subject"]},
                    {'$set': webhook_data},
                    upsert=True
                )
                app.logger.info(f'Updated MongoDB API data for chargepoint_id: {webhook_data["subject"]}')
                return True
        except Exception as e:
            app.logger.error(f"Error updating data in MongoDB for API (chargepoint_id: {webhook_data['subject']}): {e}")
            return False
    app.logger.debug("Data not related to API")
    return False


def check_longship_session(webhook_data, db):
    if "type" in webhook_data and webhook_data["type"] in ["SessionUpdate", "SessionStop", "SessionStart"]:
        app.logger.info(f"Received longship data valid for this location, processing...")
        if put_data_in_mongodb(db, webhook_data, LONGSHIP_SESSION_COLLECTION):
            return True
    app.logger.debug("Data is not related to Longship session updates")
    return False

def check_user_input(webhook_data, db):
    app.logger.info(f"Received user input valid for this location, processing...")
    if put_data_in_mongodb(db, webhook_data, USER_INPUT_COLLECTION):
        return True
    return False