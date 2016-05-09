import pandas as pd
import numpy as np

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
#data_df.head(2)



#


from copy import deepcopy
attributes_bool_atts = set()
attributes_categor_atts = {} # the attribute maps to it's values
attributes_continuous_atts = {} # this only contains the integer price range from 1 to 4, by the way
attributes_dict_atts = {} # the attribute maps to a map which contains attributes to booleans
categories_atts = set() # boolean

rest_data_df = data_df[['Restaurants' in x for x in data_df['categories']]]
print(len(rest_data_df))
     
count = 0.0
index = 0.0
from collections import defaultdict
counts = defaultdict(int)

# find the features that exist; want to expand every feature to it's own column (and get rid of categoricals)
for restaurant in rest_data_df['attributes']:
    counts[len(restaurant)] += 1
    index += 1
    for attName in restaurant:
        attVal = restaurant[attName]
        T = type(attVal)
        if T is bool:
            attributes_bool_atts.add(attName)
        elif T is unicode:
            if attName not in attributes_categor_atts:
                attributes_categor_atts[attName] = set()
            attributes_categor_atts[attName].add(attVal)
        elif T is int:
            if attName not in attributes_continuous_atts:
                attributes_continuous_atts[attName] = set()
            attributes_continuous_atts[attName].add(attVal)
        elif T is dict:
            if attName not in attributes_dict_atts:
                attributes_dict_atts[attName] = set()
            for k in attVal:
                attributes_dict_atts[attName].add(k)

for restaurant in rest_data_df['categories']:
    for category in restaurant:
        categories_atts.add(category)
        


# now insert the columns into another dataframe
rest_expanded_df = deepcopy(rest_data_df)

for attrName in attributes_bool_atts:
    rest_expanded_df.loc[:,attrName] = [int(attr[attrName]) if attrName in attr else None for attr in rest_data_df['attributes']]

for outer in attributes_categor_atts:
    for attrName in attributes_categor_atts[outer]:
        rest_expanded_df.loc[:,attrName] = [int(attr[attrName]) if attrName in attr else None for attr in rest_data_df['attributes']]

for outer in attributes_continuous_atts:
    for attrName in attributes_continuous_atts[outer]:
        rest_expanded_df.loc[:,attrName] = [int(attr[attrName]) if attrName in attr else None for attr in rest_data_df['attributes']]

for outer in attributes_dict_atts:
    for attrName in attributes_dict_atts[outer]:
        #featureName = "{}_{}".format(outer,attrName)
        rest_expanded_df.loc[:,attrName] = [int(attr[outer][attrName]) if (outer in attr and attrName in attr[outer]) else None for attr in rest_data_df['attributes']]
        
for attrName in categories_atts:
    rest_expanded_df.loc[:,attrName] = [int(attrName in r) for r in rest_data_df['categories']]
    


regression_target = rest_expanded_df['stars'].values
median = np.median(regression_target)
classification_target = [1 if stars > median else 0 for stars in regression_target]
# now that we've expanded the categorical/boolean stuff
removalList = ['attributes', 'categories', 'city','full_address','hours','latitude','longitude','name','neighborhoods',
              'open','stars','state','type']
rest_lv_df = rest_expanded_df.loc[rest_expanded_df['city']==u'Las Vegas']



#



import numpy as np

# targets for prediction
regression_target = rest_lv_df['stars'].values
median = np.median(regression_target)
classification_target = [1 if stars > median else 0 for stars in regression_target]

X = deepcopy(rest_lv_df)
y = classification_target

# now that we've expanded the categorical/boolean stuff, remove columns we won't predict on
removalList = ['attributes','business_id', 'categories', 'city','full_address','hours','latitude','longitude','name','neighborhoods',
              'open','stars','state','type']
for rm in removalList:
    X.drop(rm, axis=1, inplace=True)

X = X.fillna(0)

#df_norm = (X - X.mean()) / (X.max() - X.min())
#df_dummies.head(2)

#print X.shape

#dummy_vars = []
#dummy_vars += list(attributes_bool_atts) + attributes_categor_atts.values() + attributes_continuous_atts.values() + attributes_dict_atts.values() + list(categories_atts)






