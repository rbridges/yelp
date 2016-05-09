import json
import pandas as pd
import re
import requests
import logging

#yelp_business = pd.read_json('yelp_academic_dataset_business.json')


# read the entire file into a python array
with open('yelp_academic_dataset_business.json', 'rb') as f:
    data = f.readlines()

# remove the trailing "\n" from each line
data = map(lambda x: x.rstrip(), data)

# each element of 'data' is an individual JSON object.
# i want to convert it into an *array* of JSON objects
# which, in and of itself, is one large JSON object
# basically... add square brackets to the beginning
# and end, and have all the individual business JSON objects
# separated by a comma
data_json_str = b'[' + b','.join(data) + b']'

# now, load it into pandas
data_df = pd.read_json(data_json_str)
rest_data_df = data_df[['Restaurants' in x for x in data_df['categories']]]

zip_code = [];


for index,rest in rest_data_df.iterrows():
    lan = str(rest['latitude'])
    lon = str(rest['longitude'])
    respond = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lan+","+lon+"&result_type=postal_code&key=AIzaSyBunQHpEUVFINnt7YvGWU4MtZLctVoq2Xo").json()
    if respond.get('status') == 'OK':
        zip_code.append(int(respond['results'][0]['address_components'][0]['long_name']))
    else:
        zip_code.append(0)

