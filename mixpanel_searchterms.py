import csv
import re
import requests
import os
import json
from datetime import datetime

#define fuctions
def modifiedApiCall (api_key, url):
    api_password = 'Basic ' + api_key
    payload = {}
    headers = {
    'Authorization': api_password
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()
#strip URLs
def urlSanitize(url):
    page = re.search('(^.+)\?', url).group(1)
    page = re.sub('[0-9]+', '1', page)
    return page

print('Starting program')
#define variables
dates = [['2020-03-01', '2020-03-31']]
production_help_js_file = open("production_searches_rex.js", "r").read().strip().replace('\n', '')
production_help_api_key = os.environ.get("PRODUCTION_HELP_MIXPANEL")

for date in dates:
    print('New month')
    from_date = date[0]
    to_date = date[1]

    production_help_url = "https://mixpanel.com/api/2.0/jql?params={\"from_date\":\"" + from_date + "\", \"to_date\": \"" + to_date + "\"}&script=" + production_help_js_file
    production_data = modifiedApiCall(production_help_api_key, production_help_url)

    mixpanel_dict = {}

    for item in production_data:
        search_text = item['properties']['Search Text']
        page = item['properties']['$initial_referrer']
        if '?' in page:
            page = urlSanitize(page)
        if page not in mixpanel_dict.keys():
            mixpanel_dict[page] = {'Searches': [0, {}], 'Date': from_date.replace('-', '')}
        mixpanel_dict[page]['Searches'][0] += 1
        if search_text not in mixpanel_dict[page]['Searches'][1].keys():
            mixpanel_dict[page]['Searches'][1][search_text] = 1
        else:
            mixpanel_dict[page]['Searches'][1][search_text] += 1

print(mixpanel_dict)

with open('results.json', 'w') as file:
    json.dump(mixpanel_dict, file)