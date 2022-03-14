import requests
import json
import time


def GetEventsBatch(cursor):
    # Set the request url
    url = config['admin_api_urls']['get_events_historic']
    # Set the query string
    querystring = {"cursor":cursor}
    # Get the response
    response = requests.request("GET", url, data="", headers=headers, params=querystring)
    # Parse the response json. Output of form: {"next_cursor":"eyJ0eXBlIjoic3R...}
    response_dict = json.loads(response.text)
    # return the latest dictionary
    return response_dict

# Read the config file to the dictionary
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

#Set Header in Prepartion to call the Events API
headers = {'Authorization': "Bearer " + config['organization']['access_token']}

#First, get the initial cursor
# Set the request url
url = config['admin_api_urls']['get_new_cursor_historic']
# Set the query string
querystring = {"company_id":config['organization']['company_id'],"since_timestamp":1577941200100100,"until_timestamp":1583125200100100}
# Get the response
response = requests.request("GET", url, headers=headers, params=querystring)
# Parse the response json. Output of form: {"next_cursor":"eyJ0eXBlIjoic3R...}
response_dict = json.loads(response.text)
# Isolate the cursor
cursor = response_dict['next_cursor']
# Set initial value of moreToRead to guarantee we do at least one read
moreToRead=True
# Loop through all required pages
eventCounter = 0
while moreToRead:
    # Get the next set of events
    response_dict = GetEventsBatch(cursor)
    # Dump the events to splunk (or elsewhere)
    splunk_data = json.dumps(response_dict['events'])
    print(splunk_data)
    eventCounter = eventCounter + len(response_dict['events'])
    # Do we have additional pages of events to read?
    moreToRead = response_dict['more_to_read']
    if moreToRead:
        # Set the cursor for the next call
        cursor = response_dict['next_cursor']
    # Avoid rate limiting
    time.sleep(10)
# print(eventCounter)




