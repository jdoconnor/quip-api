# Splunk Setup - Generic



```
    "company_id": "",
    "refresh_token": "",
    "grant_type": "",
    "client_id": "",
    "client_secret": "",
    "access_token": "",
    "cursor": ""
```

|Script	|Purpose	|Suggested Frequency	|
|[quipeventsapihistoric.py](./quipeventsapihistoric.py)|Retrieve a historic set set of events based on a specificed start and end date <br/>These dates are set by specifying the epoch time in microseconds: see - https://www.freeformatter.com/epoch-timestamp-to-date-converter.html <br/>Script can easily be altered to convert a stardard date to epoch time as necessary.<br/>Note: two new config entries are required in the "admin_api_urls" section: "get_new_cursor_historic", and "get_events_historic"	|As required, can be run once every 24h to replace to quipeventsapi.py real time script	|
| [quipeventsapi.py](./quipeventsapi.py) 	|Retrieve events from the Quip Events API, and dump them to splunk	|Once every 60s	|
| [quipthreads.py](./quipthreads.py) 	|Retrieve the complete list of Quip thread meta-data from the Quip Admin API, and save them to a lookup table. <br/>**Update (Monday, Mar 14, 2022): Added support for shared_folder_ids in csv export** <br/> **Update (Monday, June 1, 2020): added paging support for >1000 thread count.**<br/>**Update (Thursday, May 28, 2020): added ability to set batch size for Get Thread.**|Once every 12h	|
| [quipusers.py](./quipusers.py) 	|Retrieve the complete list of Quip user meta-data from the Quip Admin API, and save them to a lookup table	|Once every 24h	|
| [refreshtoken.py](./refreshtoken.py) 	|Refeshes the OAuth 2 access token	|Once every 29 days	|
| [config.json](./config.json) 	|Config file - has been pre-loaded with the data above.<br/>**Update (Thursday, June 18, 2020): added support for historic event calls.**<br/>**Update (Thursday, May 28, 2020): added new setting to configure batch size for Get Thread.**	|N/A	|
| [docsscanner.py](./docscanner.py) 	|Script to convert the spreadsheet in the "Main tab" tab of the "Static then reference" spreadsheet. Please note that changing the name of the "Main tab" will require a script change.	|As required	|
