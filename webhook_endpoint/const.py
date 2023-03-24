import os

# Get the environment variables
MONGODB_URL = os.getenv("ME_CONFIG_MONGODB_URL", "mongodb://root:example@mongo:27017/")
AUTH_KEY = os.getenv("AUTHENTICATION_KEY", "test")
DB_NAME = os.getenv("DB_NAME", "webhook_data")
USER_INPUT_COLLECTION = os.getenv("USER_INPUT_COLLECTION", "user_input")
LONGSHIP_COLLECTION = os.getenv("LONGSHIP_COLLECTION", "longshipid")

# Define constants for HTTP status codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_INTERNAL_SERVER_ERROR = 500

# Map userinputid and longshipid to corresponding collections used to put the data in the correct collection
COLLECTION_MAP = {
    'userinputid': USER_INPUT_COLLECTION,
    'longshipid': LONGSHIP_COLLECTION
}