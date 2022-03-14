import requests
import json
from datetime import datetime
from datetime import date

def GetThreads(page):
    #Set Header
    headers = {'Authorization': "Bearer " + config['organization']['access_token']}
    # Set the request url
    url = config['admin_api_urls']['get_all_threads_list']
    # Set the query string
    querystring = {"company_id":config['organization']['company_id'],"page":page}
    # Get the reponse
    response = requests.request("POST", url, data="", headers=headers, params=querystring)
    # Load response to dictionary
    response_dict = json.loads(response.text)
    # Return
    return response_dict

# Important: Please set this to the correct path
configFilePath = 'config.json'

# Read the config file to the dictionary
with open(configFilePath) as json_data_file:
    config = json.load(json_data_file)

# Make First Call to Get Threads
page=0
moreToRead=True
response_dict = GetThreads(page)
# Are there more pages to read?
try:
    page = response_dict['next_page']
except:
    moreToRead=False

while moreToRead:
    next_page_response_dict = GetThreads(page)
    response_dict['thread_ids'] += next_page_response_dict['thread_ids']
    try:
        page = next_page_response_dict['next_page']
    except:
        moreToRead=False

# Create a string array to house batches of threads
thread_array = ['']
array_index = 0
# Assemble the threads as batch array
thread_counter = 0 
for thread_id in response_dict['thread_ids']:  
    thread_array[array_index] += (thread_id + ',')
    thread_counter += 1
    if (thread_counter >= config['general_params']['thread_batch_call_size']):
        thread_array[array_index] = thread_array[array_index].rstrip(',')
        thread_array.append('')
        array_index += 1
        thread_counter = 0
thread_array[array_index] = thread_array[array_index].rstrip(',')
# Create new Quip User csv
filename = config['lookup_file_paths']['quip_threads']+str(datetime.today().strftime("%Y%m%d%H%M%S"))+'.csv'   
with open(filename,'w') as f:
    # Write the headers of the CSV
    f.write("\"author_id\",\"thread_class\",\"id\",\"created_usec\",\"updated_usec\",\"title\",\"link\",\"type\",\"document_id\",\"is_deleted\",\"shared_folder_ids\"") 
    for thread_ids in thread_array:
        if len(thread_ids) > 0:
            # Now get all the thread info
            headers = {'Authorization': "Bearer " + config['organization']['access_token']}
            # Set the request url
            url_thread = config['admin_api_urls']['get_thread']
            # Set the query string
            querystring_thread = {"company_id":config['organization']['company_id'],"ids":thread_ids}
            # Get the reponse
            response_thread = requests.request("GET", url_thread, data="", headers=headers, params=querystring_thread)
            # Parse the response to the dictionary
            response_thread_dict = json.loads(response_thread.text)
            # Add all the theads to the CSV file
            for thread in response_thread_dict:
                current_thread = response_thread_dict[thread]
                try:
                    author_id = current_thread['thread']['author_id']
                except:
                    author_id = ''
                try:
                    thread_class = current_thread['thread']['thread_class']
                except:
                    thread_class = ''
                try:
                    id_ = current_thread['thread']['id']
                except:
                    id_ = ''
                try:
                    created_usec = str(current_thread['thread']['created_usec'])
                except:
                    created_usec = ''
                try:
                    updated_usec = str(current_thread['thread']['updated_usec'])
                except:
                    updated_usec = ''
                try:
                    title = current_thread['thread']['title']
                except:
                    title = ''
                try:
                    link = current_thread['thread']['link']
                except:
                    link = ''
                try:
                    type_ = current_thread['thread']['type']
                except:
                    type_ = ''
                try:
                    document_id = current_thread['thread']['document_id']
                except:
                    document_id = ''
                try:
                    is_deleted = str(current_thread['thread']['is_deleted'])
                except:
                    is_deleted = ''
                shared_folder_ids = ''
                for folder_id in current_thread['shared_folder_ids']:
                    shared_folder_ids += folder_id + ','
                if len(shared_folder_ids) > 0:
                    shared_folder_ids = shared_folder_ids[:-1]

                f.write("\n\""+author_id+"\",\""+thread_class+"\",\""+id_+"\",\""+created_usec+"\",\""+updated_usec+"\",\""+title+"\",\""+link+"\",\""+type_+"\",\""+document_id+"\",\""+is_deleted+"\",\""+shared_folder_ids+"\"")
                print("\n\""+author_id+"\",\""+thread_class+"\",\""+id_+"\",\""+created_usec+"\",\""+updated_usec+"\",\""+title+"\",\""+link+"\",\""+type_+"\",\""+document_id+"\",\""+is_deleted+"\",\""+shared_folder_ids+"\"")


