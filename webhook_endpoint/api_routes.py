from flask import Blueprint, jsonify, current_app as app
from const import CHARGEPOINT_IDS
from webhook_handler import api_data
from bson import json_util
import json

api_blueprint = Blueprint('api', __name__)

# Add the url prefix to each item in the list
url_list = [f"/api/chargepointstatus/{item}" for item in CHARGEPOINT_IDS]

# Function to handle the route for each URL in the list
def route_handler(chargepointid):
    app.logger.info(f'Accessing API endpoint for chargepoint_id: {chargepointid}')
    chargepoint_collection = app.config['db']['chargepoints']
    data = chargepoint_collection.find_one({'chargepoint_id': chargepointid})
    if data:
        # Serialize data to JSON using pymongo's json_util
        json_data = json_util.dumps(data)
        # Convert JSON string to Python dictionary using json.loads
        parsed_data = json.loads(json_data)
        return jsonify(parsed_data)
    else:
        return jsonify({'message': f'No data available for {chargepointid}'})
    
# Iterate through the list of URLs and create an endpoint for each
for index, url in enumerate(url_list):
    key = url.split('/')[-1]  # Get the last part of the URL as a key
    endpoint_name = f'route_handler_{index}'
    api_blueprint.add_url_rule(url, endpoint_name, lambda key=key: route_handler(key), methods=['GET'])

if __name__ == '__main__':
    api_blueprint.run(debug=True)
