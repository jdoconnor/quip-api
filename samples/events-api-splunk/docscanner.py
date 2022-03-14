import requests
import json
from datetime import datetime
from datetime import date
from bs4 import BeautifulSoup
import csv

# Important: Please set this to the correct path
configFilePath = 'config.json'
# Important: Please set this to the correct thread id
thread = "Gm7fAgW5vHTh"

# Read the config file to the dictionary
with open(configFilePath) as json_data_file:
    config = json.load(json_data_file)

# Now get all the thread info
headers = {'Authorization': "Bearer " + config['organization']['access_token']}
# Set the request url
url_thread = config['admin_api_urls']['get_thread']
# Set the query string
querystring_thread = {"company_id":config['organization']['company_id'],"ids":thread}
# Get the reponse
response_thread = requests.request("GET", url_thread, data="", headers=headers, params=querystring_thread)
# Parse the response to the dictionary
response_thread_dict = json.loads(response_thread.text)

# Isolate the row
soup = BeautifulSoup(response_thread_dict['Gm7fAgW5vHTh']['html'])
table = soup.find('table', attrs={'title':'Main tab'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')

# Dump the output to CSV
with open('output'+str(datetime.today().strftime("%Y%m%d%H%M%S"))+'.csv', 'w') as myfile:
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(cols)


