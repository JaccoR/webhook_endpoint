from pywebhook import check_environment_variables, connect_to_mongodb, app

# Check environment variables and connect to MongoDB
check_environment_variables()
connect_to_mongodb()

if __name__ == '__main__':
    # Start webserver 
    app.run()