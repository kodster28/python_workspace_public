import csv
import re
import requests
import os
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
dates = [['2020-06-01', '2020-06-30']]
production_help_js_file = open("production_help_page_level_fex.js", "r").read().strip().replace('\n', '')
production_help_api_key = os.environ.get("PRODUCTION_HELP_MIXPANEL")
legacy_help_js_file = open("legacy_help_page_level_fex.js", "r").read().strip().replace('\n', '')
legacy_help_api_key = os.environ.get("LEGACY_HELP_MIXPANEL")

column_headers = ['Page', 'Help Views', 'Searches', 'Chat', 'Knowledgebase', 'Case Central', 'Community', 'Training Central', 'Date']

with open(r"C:\Users\kody.jackson\Desktop\mixpanel.csv", mode='w', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(column_headers)

    for date in dates:
        print('New month')
        from_date = date[0]
        to_date = date[1]

        production_help_url = "https://mixpanel.com/api/2.0/jql?params={\"from_date\":\"" + from_date + "\", \"to_date\": \"" + to_date + "\"}&script=" + production_help_js_file
        legacy_help_url = "https://mixpanel.com/api/2.0/jql?params={\"from_date\":\"" + from_date + "\", \"to_date\": \"" + to_date + "\"}&script=" + legacy_help_js_file
        production_data = modifiedApiCall(production_help_api_key, production_help_url)
        legacy_data = modifiedApiCall(legacy_help_api_key, legacy_help_url)

        mixpanel_dict = {}

        for item in production_data:
            page = item['properties']['$initial_referrer']
            if '?' in page:
                page = urlSanitize(page)
            if page not in mixpanel_dict.keys():
                mixpanel_dict[page] = {'Navigate to  Case Central': 0, 'Navigate to  Community': 0,
                                       'Navigate to  Knowledgebase': 0, 'Navigate to  Training Central': 0, 'Open Support Chat': 0, 'Searches': 0,
                                       'Help Widget': 0, 'Date': from_date.replace('-', '')}
            if item['name'] == 'Button':
                try:
                    button = item['properties']['Button Name']
                    mixpanel_dict[page][button] += 1
                except:
                    continue
            elif item['name'] == 'Search':
                mixpanel_dict[page]['Searches'] += 1

        for item in legacy_data:
            page = item['key'][0]
            if '?' in page:
                page = urlSanitize(page)
            if page in mixpanel_dict.keys():
                mixpanel_dict[page]['Help Widget'] += item['value']

        for key, value in mixpanel_dict.items():
            data_writer.writerow([key, value['Help Widget'], value['Searches'], value['Open Support Chat'], value['Navigate to  Knowledgebase'], value['Navigate to  Case Central'], value['Navigate to  Community'], value['Navigate to  Training Central'], value['Date']])

        print("Finished one month")
