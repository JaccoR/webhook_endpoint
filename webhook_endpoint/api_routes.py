from flask import Blueprint, jsonify, current_app as app
from const import CHARGEPOINT_IDS, HTTP_NO_CONTENT, HTTP_INTERNAL_SERVER_ERROR, LONGSHIP_SESSION_STATUS_COLLECTION
from bson import json_util
import json

api_blueprint = Blueprint('api', __name__)

# Add the url prefix to each item in the list
url_list = [f"/api/chargepointstatus/{item}" for item in CHARGEPOINT_IDS]

# Function to handle the route for each URL in the list
def route_handler(chargepointid):
    try:
        app.logger.info(f'Accessing API endpoint for chargepointid: {chargepointid}')
        chargepoint_collection = app.config['db'][LONGSHIP_SESSION_STATUS_COLLECTION]
        data = chargepoint_collection.find_one({'subject': chargepointid})
        if data:
            app.logger.info(f'Data found for chargepointid: {chargepointid}')
            json_data = json_util.dumps(data)  # Serialize the data using json_util.dumps()
            parsed_data = json.loads(json_data)  # Load the serialized data back into a Python dict
            return jsonify(parsed_data)
        else:
            app.logger.warning(f'No data available for chargepointid: {chargepointid}')
            return jsonify({'message': f'No data available for {chargepointid}'}), HTTP_NO_CONTENT
    except Exception as e:
        app.logger.error(f"Error processing request for chargepointid: {chargepointid}: {e}")
        return jsonify({'message': 'An error occurred while processing your request.'}), HTTP_INTERNAL_SERVER_ERROR

    
# Iterate through the list of URLs and create an endpoint for each
for index, url in enumerate(url_list):
    key = url.split('/')[-1]  # Get the last part of the URL as a key
    endpoint_name = f'route_handler_{index}'
    # Attach route handler function to the specific chargepointid
    api_blueprint.add_url_rule(url, endpoint_name, lambda key=key: route_handler(key), methods=['GET'])

