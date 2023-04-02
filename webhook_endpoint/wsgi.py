from webhook_handler import app
from startup_tasks import check_environment_variables, connect_to_mongodb
from api_routes import api_blueprint  # Import the api_blueprint from api_routes.py

# Run startup tasks
check_environment_variables()

# Connect to MongoDB and get the database object
db = connect_to_mongodb()

# Attach the db object to the Flask app
app.config['db'] = db

# Register the API Blueprint
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    # Start webserver
    app.run()
