from pywebhook import app
from startup_tasks import check_environment_variables, connect_to_mongodb

# Run startup tasks
check_environment_variables()

# Connect to MongoDB and get the database object
db = connect_to_mongodb()

# Attach the db object to the Flask app
app.config['db'] = db

if __name__ == '__main__':
    # Start webserver
    app.run()
