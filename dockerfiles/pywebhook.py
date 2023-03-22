import logging
from flask import Flask, request
from pymongo import MongoClient

# Import variables from environment.py
from environment import MONGODB_URL, AUTH_KEY, DB_NAME, USER_INPUT_COLLECTION, LONGSHIP_COLLECTION

# Init Flask app
app = Flask(__name__)

# Set up logging
app.logger.setLevel(logging.INFO)

# Connect to MongoDB
try:
    mongo_client = MongoClient(MONGODB_URL)
    db = mongo_client[DB_NAME]
    app.logger.info(f'Connected with MongoDB')
    
except Exception as e:
    app.logger.error(f"Error connecting to MongoDB: {e}")
    exit(1)

# Check that required environment variables are set
@app.before_first_request
def check_environment_variables():
    if not MONGODB_URL:
        app.logger.error("MongoDB URL not set")
        exit(1)

    if not AUTH_KEY:
        app.logger.error("Authentication key not set")
        exit(1)

# Save data to the appropriate MongoDB collection
def save_data_to_mongodb(data, db):
    # User Input set collection
    if "userinputid" in data:
        collection = USER_INPUT_COLLECTION
    # Longship set collection
    elif "longshipid" in data:
        collection = LONGSHIP_COLLECTION
    # Check invalid data
    else:
        app.logger.warning(f"Invalid data: {data}")
        return 'Invalid data', 400

    # Try to put data in mongoDB
    try:
        db[collection].insert_one(data)
        app.logger.info(f'Successfully inputted data into the {collection} collection')
        return 'OK', 200
    except Exception as e:
        app.logger.error(f"Error inserting data into MongoDB: {e}")
        return 'Error', 500

# Define the webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    # Check if the authentication key matches the expected value
    header_auth_key = request.headers.get('authentication')
    if header_auth_key != AUTH_KEY:
        app.logger.warning(f"Authentication failed: Invalid key: {header_auth_key}")
        return 'Authentication failed', 401

     # Parse the JSON data from the request body and save to MongoDB
    data = request.json
    response, status_code = save_data_to_mongodb(data, db)
    return response, status_code



























