import pandas as pd
import numpy as np
import requests, json
import sys
import os

client_id = os.environ['BNET_CLIENT_ID']
client_secret = os.environ['BNET_SECRET']

def create_access_token(client_id, client_secret, region = 'us'):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))
    return response.json()

token = create_access_token(client_id, client_secret)['access_token']
print(token)

# Get Specializations Index
spec_index = requests.get(f'https://us.api.blizzard.com/data/wow/playable-specialization/index?namespace=static-us&locale=en_US&access_token={token}').json()

spec_dict = {}

for i in spec_index['character_specializations']:
    spec_dict[i['id']] = {'name':i['name']}

spec_df = pd.DataFrame.from_dict(spec_dict, orient='index')
spec_df.index.name = 'id'

# Add Class Name

class_id_dict = {}
for i in spec_df.index:
    spec_class = requests.get(f'https://us.api.blizzard.com/data/wow/playable-specialization/{i}?namespace=static-us&locale=en_US&access_token={token}').json()
    class_id_dict[i] = {'class_name':spec_class['playable_class']['name']}

class_id_df = pd.DataFrame.from_dict(class_id_dict, orient='index')
class_id_df.index.name = 'id'

spec_df = spec_df.join(class_id_df)

# Add Spec Media
spec_media_dict = {}

for i in spec_df.index:
    spec_media = requests.get(f'https://us.api.blizzard.com/data/wow/media/playable-specialization/{i}?namespace=static-us&locale=en_US&access_token={token}').json()
    spec_media_dict[i] = {'spec_media':spec_media['assets'][0]['value']}

spec_media_df = pd.DataFrame.from_dict(spec_media_dict, orient='index')
spec_media_df.index.name = 'id'

spec_df = spec_df.join(spec_media_df)

spec_df.to_csv('spec_df.csv')
