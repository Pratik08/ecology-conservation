import re
import csv
import tqdm
import json
import numpy as np
import pandas as pd


def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False


'''
Preprocessing to remove grants which are empty, operating support,
program support, etc.
'''
data = pd.read_csv('./Data/AllData - AllData.csv')
data = data.drop([ele for ele in data.columns.to_list()
                  if ele not in ['Description']], axis=1)
data = data.dropna().reset_index(drop=True)
data = data[data.Description != 'For general operating support']
data = data[data.Description != 'For General Operating Support']
data = data[data.Description != 'For operating support']
data = data[data.Description != 'Charitable']
data = data[data.Description != "For the organization's charitable use"]
data = data[data.Description != 'For capital support']
data = data[data.Description != 'For annual support']
data = data[data.Description != 'For annual giving']
data = data[data.Description != 'For general support']
data = data[data.Description != 'OPERATING']
data = data[data.Description != 'For operating support']
data = data[data.Description != 'Operating']
data = data[data.Description != 'OPERATIONAL SUPPORT']
data = data[data.Description != 'Operational support']
data = data[data.Description != 'General Operating Support']
data = data[data.Description != 'General purposes']
data = data[data.Description != 'General purpose']
data = data[data.Description != 'General']
data = data[data.Description != 'Support']
data = data[data.Description.str.lower() != 'general support']
data = data[data.Description.str.lower() != 'for general support']
data = data[data.Description.str.lower() != 'general operating']
data = data[data.Description.str.lower() != 'for general operating']
data = data[data.Description.str.lower() != 'for capital']
data = data[data.Description.str.lower() != 'general operating support']
data = data[data.Description.str.lower() != 'for program support']

data_sentences = data.Description.values.tolist()
# data_sentences = [x.lower() for x in data_sentences]

'''
Reading all locations from file
'''
with open('./Data/world-cities_json.json') as f:
    cities_data = json.load(f)

countries = []
us_cities = []
grant_locations = []

us_state_codes = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL",
                  "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
                  "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
                  "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
                  "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI",
                  "WY"]
# us_state_codes = [x.lower() for x in us_state_codes]

us_states = ['Alaska', 'Alabama', 'Arkansas', 'American Samoa', 'Arizona',
             'California', 'Colorado', 'Connecticut', 'District of Columbia',
             'Delaware', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Iowa',
             'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana',
             'Massachusetts', 'Maryland', 'Maine', 'Michigan', 'Minnesota',
             'Missouri', 'Northern Mariana Islands', 'Mississippi', 'Montana',
             'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire',
             'New Jersey', 'New Mexico', 'Nevada', 'New York', 'Ohio',
             'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico',
             'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
             'Texas', 'Utah', 'Virginia', 'Virgin Islands', 'Vermont',
             'Washington', 'Wisconsin', 'West Virginia', 'Wyoming']
us_states = [x.lower() for x in us_states]

continents = ['europe', 'asia', 'antarctica', 'australia', 'africa',
              'north america', 'south america']

regions = ['america', 'americas', 'eurasia', 'oceania', 'mesoamerica']

for ele in cities_data:
    if ele['country'] == 'United States':
        us_cities.append(ele['name'].lower())
    else:
        countries.append(ele['country'].lower())

us_cities = list(set(us_cities))
countries = list(set(countries))

pbar = tqdm.tqdm(total=len(data_sentences))
for grant in data_sentences:
    temp_loc = []

    for keyword in us_state_codes:
        if string_found(keyword, grant):
            temp_loc.append(keyword.replace(' ', '_'))
    grant = grant.lower()

    for keyword in us_states:
        if string_found(keyword, grant):
            temp_loc.append(keyword.replace(' ', '_'))

    for keyword in continents:
        if string_found(keyword, grant):
            temp_loc.append(keyword.replace(' ', '_'))

    for keyword in regions:
        if string_found(keyword, grant):
            temp_loc.append(keyword.replace(' ', '_'))

    for keyword in countries:
        if string_found(keyword, grant):
            temp_loc.append(keyword.replace(' ', '_'))

#     for keyword in us_cities:
#         if string_found(keyword, grant):
#             temp_loc.append(keyword.replace(' ', '_'))

    temp_loc = list(set(temp_loc))
    grant_locations.append(temp_loc)

    pbar.update(1)
pbar.close()

output_grants = []

print('Formatting output')
pbar = tqdm.tqdm(total=len(data_sentences))
for idx in range(len(data_sentences)):
    temp = []
    temp.append(data_sentences[idx])
    temp.append("|".join(grant_locations[idx]))
    output_grants.append(temp)
    pbar.update(1)
pbar.close()

print('Saving output file')
with open("./Data/Output/output_grants_location_v2.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output_grants)
