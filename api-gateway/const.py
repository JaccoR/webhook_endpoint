import os

# Get the environment variables
MONGODB_URL = os.getenv("ME_CONFIG_MONGODB_URL", "mongodb://root:example@mongo:27017/")
AUTH_KEY = os.getenv("AUTHENTICATION_KEY", "test")
DB_NAME = os.getenv("DB_NAME", "webhook_data")
USER_INPUT_COLLECTION = os.getenv("USER_INPUT_COLLECTION", "user_input")
LONGSHIP_SESSION_COLLECTION = os.getenv("LONGSHIP_JOB_COLLECTION", "longship_jobs")
LONGSHIP_SESSION_STATUS_COLLECTION = os.getenv("LONGSHIP_SESSION_STATUS_COLLECTION", "sessions_status")
CHARGEPOINT_IDS = os.getenv('CHARGEPOINT_IDS').split(', ')

# Define constants for HTTP status codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_NO_CONTENT = 204

# Map userinputid and longshipid to corresponding collections used to put the data in the correct collection
COLLECTION_MAP = {
    'userinputid': USER_INPUT_COLLECTION,
    'specversion': LONGSHIP_SESSION_COLLECTION
}

# Some util
LOG_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S %z'