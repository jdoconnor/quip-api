import requests
import json
from datetime import datetime
from datetime import date

# Important: Please set this to the correct path
configFilePath = 'config.json'

# Read the config file to the dictionary
with open(configFilePath) as json_data_file:
    config = json.load(json_data_file)

#Set Header
headers = {'Authorization': "Bearer " + config['organization']['access_token']}
# Set the request url
url = config['admin_api_urls']['get_users']
# Set the query string
querystring = {"company_id":config['organization']['company_id']}
# Get the reponse
response = requests.request("POST", url, data="", headers=headers, params=querystring)
# Load response to dictionary
response_dict = json.loads(response.text)
# Create new Quip User csv
filename = config['lookup_file_paths']['quip_users']+str(datetime.today().strftime("%Y%m%d%H%M%S"))+'.csv'
with open(filename,'w') as f:
    # Write the headers of the CSV
    f.write("\"user_id\",\"name\",\"email_address\"")
    # Isolate the new thread
    for user in response_dict:
        name = response_dict[user]['name']
        id = response_dict[user]['id']
        email = response_dict[user]['emails'][0]['address']
        # Write user to csv
        f.write("\n\""+id+"\",\""+name+"\",\""+email+"\"")
