import os

MONGODB_URL = os.getenv("ME_CONFIG_MONGODB_URL", "mongodb://root:example@mongo:27017/")
AUTH_KEY = os.getenv("AUTHENTICATION_KEY", "test")
DB_NAME = os.getenv("DB_NAME", "webhook_data")
USER_INPUT_COLLECTION = os.getenv("USER_INPUT_COLLECTION", "user_input")
LONGSHIP_COLLECTION = os.getenv("LONGSHIP_COLLECTION", "longshipid")
