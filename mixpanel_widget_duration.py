import csv
import re
import json
import os
from statistics import mean, stdev


def urlSanitize(url):
    page = re.search('(^.+)\?', url).group(1)
    page = re.sub('[0-9]+', '1', page)
    return page


directory = r'C:/Users/kody.jackson/Documents/Help_Widget/'
entries = os.listdir(directory)
homePages = ['https://renxt.blackbaud.com/home', 'https://renxt.blackbaud.com/',
             'https://host.nxt.blackbaud.com/renxt-homepage/',
             'https://renxt.blackbaud.com/fundraising/workcenter/fundraisers/me/overview']

homeList = []
otherList = []
total_sessions = 0
user_count = 1
userDict = {}

for entry in entries:
    print("Starting new JSON file")
    with open(os.path.join(directory, entry)) as json_file:
        data = json.load(json_file)

    groupedByUser = sorted(data, key=lambda k: k['user'])

    for num, item in enumerate(groupedByUser, start=0):

        if (num == len(groupedByUser) - 1):
            break
        if groupedByUser[num]['user'] not in userDict:
            userDict.update({groupedByUser[num]['user']: {}})
            userDict[groupedByUser[num]['user']].update(
                {'total_session': 0, 'home_session': 0, 'home_long_session': 0, 'home_quick_session': 0,
                 'other_session': 0, 'other_long_session': 0, 'other_quick_session': 0})
            user_count += 1
        if groupedByUser[num]['action'] == 'Opened From Invoker' and groupedByUser[num + 1][
            'action'] == 'Closed From Invoker' and groupedByUser[num]['user'] == groupedByUser[num + 1]['user']:
            total_sessions += 1
            userDict[groupedByUser[num]['user']]['total_session'] += 1
            duration = abs(groupedByUser[num]['time'] - int(groupedByUser[num + 1]['time'])) / 1000
            if duration <= 1200:
                pageUrl = urlSanitize(item['page'])
                if pageUrl in homePages:
                    homeList.append(duration)
                    userDict[groupedByUser[num]['user']]['home_session'] += 1
                    if duration <= 8:
                        userDict[groupedByUser[num]['user']]['home_quick_session'] += 1
                    else:
                        userDict[groupedByUser[num]['user']]['home_long_session'] += 1
                else:
                    otherList.append(duration)
                    userDict[groupedByUser[num]['user']]['other_session'] += 1
                    if duration <= 8:
                        userDict[groupedByUser[num]['user']]['other_quick_session'] += 1
                    else:
                        userDict[groupedByUser[num]['user']]['other_long_session'] += 1

homeDurationAvg = mean(homeList)
homeDurationSTDEV = stdev(homeList)
homeWidgetSessions = len(homeList)
otherDurationAvg = mean(otherList)
otherDurationSTDEV = stdev(otherList)
otherWidgetSessions = len(otherList)

print('Total users')
print(user_count)

print("Total sessions")
print(total_sessions)

print("Home pages overall")
print(homeDurationAvg, homeDurationSTDEV, homeWidgetSessions)

print('Other pages overall')
print(otherDurationAvg, otherDurationSTDEV, otherWidgetSessions)

home_ratio = 0
other_ratio = 0
total_active_users = 0

for key, value in userDict.items():
    if value['total_session'] >= 10:
        total_active_users += 1
        try:
            if value['home_quick_session'] <= value['home_long_session']:
                home_ratio += 1
            elif value['other_quick_session']  <= value['other_long_session']:
                other_ratio += 1
        except:
            print('Divided by zero')


print("Values")
print(total_active_users)
print(home_ratio)
print(home_ratio / total_active_users)
print(other_ratio)
print(other_ratio / total_active_users)

quit()
column_headers = ['User', 'Total Sessions', 'Home Sessions', 'Home Long Sessions', 'Home Quick Sessions',
                  'Other Sessions', 'Other Long Sessions', 'Other Quick Sessions']

with open(r"C:\Users\kody.jackson\Desktop\mixpanel-widget-data.csv", mode='w', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(column_headers)

    for key, value in userDict.items():
        data_writer.writerow([key, value['total_session'], value['home_session'], value['home_long_session'],
                              value['home_quick_session'], value['other_session'], value['other_long_session'],
                              value['other_quick_session']])
