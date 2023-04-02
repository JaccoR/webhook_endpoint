import logging
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from const import MONGODB_URL, AUTH_KEY, DB_NAME, LOG_FORMAT, DATE_FORMAT, CHARGEPOINT_IDS

# Set up logging
logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)

# Check if the required environment variables are set
def check_environment_variables():
    if not MONGODB_URL:
        logging.error("MongoDB URL not set")
        exit(1)

    if not AUTH_KEY:
        logging.error("Authentication key not set")
        exit(1)

    if not CHARGEPOINT_IDS:
        logging.error("No charegepoints set")
        exit(1)

# Connect to MongoDB and test connection
def connect_to_mongodb():
    try:
        mongo_client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000, maxPoolSize=50)
        mongo_client.server_info()
        db = mongo_client[DB_NAME]
        logging.info(f'Connected with MongoDB')
        return db
    except ServerSelectionTimeoutError as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        exit(1)

