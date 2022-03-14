import requests
import json
from datetime import datetime
from datetime import date

# Important: Please set this to the correct path
configFilePath = 'config.json'

# Read the config file to the dictionary
with open(configFilePath) as json_data_file:
    config = json.load(json_data_file)

# Set the request url
url = config['admin_api_urls']['refresh_token']
# Set the query string
querystring = {"grant_type":config['organization']['grant_type'],"refresh_token":config['organization']['refresh_token'],"client_id":config['organization']['client_id'],"client_secret":config['organization']['client_secret']}
# Get the response
response = requests.request("GET", url, params=querystring)
# Parse the response json
response_dict = json.loads(response.text)
#Isolate and save the new Access Token
config['organization']['access_token'] = response_dict['access_token']
# Write the token to the config file
with open(configFilePath, 'w') as outfile:
    json.dump(config, outfile)