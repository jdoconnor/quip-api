import requests
import json

# Important: Please set this to the correct path
configFilePath = 'config.json'

# Read the config file to the dictionary
with open(configFilePath) as json_data_file:
    config = json.load(json_data_file)

#Set Cursor and Header in Prepartion to call the Events API
cursor = config['organization']['cursor']
headers = {'Authorization': "Bearer " + config['organization']['access_token']}

# Have we got a cursor?
if (len(cursor) == 0):
    # Set the request url
    url = config['admin_api_urls']['get_new_cursor']
    # Set the query string
    querystring = {"company_id":config['organization']['company_id']}
    # Get the response
    response = requests.request("GET", url, headers=headers, params=querystring)
    # Parse the response json. Output of form: {"next_cursor":"eyJ0eXBlIjoic3R...}
    response_dict = json.loads(response.text)
    # Isolate the cursor
    config['organization']['cursor'] = response_dict['next_cursor']
    # Write the cursor to the config file
    with open(configFilePath, 'w') as outfile:
        json.dump(config, outfile)
else:
    # Set the request url
    url = config['admin_api_urls']['get_events']
    # Set the query string
    querystring = {"cursor":cursor}
    # Get the response
    response = requests.request("GET", url, data="", headers=headers, params=querystring)
    # Parse the response json. Output of form: {"next_cursor":"eyJ0eXBlIjoic3R...}
    response_dict = json.loads(response.text)
    # Successful Call?
    if response.status_code == 200:
        # Isolate the cursor
        config['organization']['cursor'] = response_dict['next_cursor']
        # Write the cursor to the config file
        with open(configFilePath, 'w') as outfile:
            json.dump(config, outfile)
        # Dump data to splunk
        splunk_data = json.dumps(response_dict['events'])
        print(splunk_data)



